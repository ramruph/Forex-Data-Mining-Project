import pandas as pd
import requests
import defs
import utils
from dateutil.parser import *

class OandaAPI():

    def __init__(self):
        self.session = requests.Session()

    def fetch_instruments(self):
        url = f"{defs.OANDA_URL}/accounts/{defs.ACCOUNT_ID}/instruments/"
        response = self.session.get(url, params=None, headers = defs.SECURE_HEADER)
        return response.status_code, response.json()


    def get_intruments_df(self):
        code, data = self.fetch_instruments()
        if code == 200:
            df = pd.DataFrame.from_dict(data['instruments'])
            return df[['name', 'type','displayName','pipLocation','marginRate']]
        else:
            return None
    
    def save_instruments(self):
        df = self.get_intruments_df()
        if df is not None:
            df.to_pickle(utils.get_instrument_data_filename())


    def fetch_candles(self, pair_name, count=None, granularity="H1", date_from=None, date_to=None, as_df=False):
        url = f"{defs.OANDA_URL}/instruments/{pair_name}/candles"
        params = dict(
            count = count, 
            granularity = granularity,
            price = "MBA"
        )
        if date_from is not None and date_to is not None:
            params['to'] = int(date_to.timestamp())
            params['from'] = int(date_from.timestamp())
        elif count is not None:
            params['count'] = count
        else:
            params['count'] = 300
        response = self.session.get(url, params=params, headers = defs.SECURE_HEADER)
        #Error Handling
        if response.status_code != 200:
            return response.status_code, None
        

        if as_df== True:
            json_data = response.json()['candles']
            return response.status_code, OandaAPI.candles_to_df(json_data)
        else:
            
            return response.status_code, response.json()
    
    @classmethod
    def candles_to_df(cls, json_data):
        prices = ['mid', 'bid', 'ask']
        ohlc = ['o','h','l','c']
        our_data = []
        for candle in json_data:
            if candle['complete'] == False: # We only want to look at the candles that are closed so complete== True
                continue
            new_dict={}
            new_dict['time'] = candle['time']
            new_dict['volume'] = candle['volume']
            for price in prices:
                for oh in ohlc:
                    new_dict[f"{price}_{oh}"] = float(candle[price ][oh])
            our_data.append(new_dict)
        df = pd.DataFrame.from_dict(our_data)
        df['time'] = [parse(x) for x in df.time]

        return df
    

if __name__ == '__main__':
    api = OandaAPI()
    date_from = utils.get_utc_dt_from_string("2020-05-05 18:00:00")
    date_to = utils.get_utc_dt_from_string("2020-05-06 18:00:00")

    response,df = api.fetch_candles("EUR_USD", date_from=date_from, date_to=date_to, as_df=True)
    # api.save_instruments()
    print(df.info())