import pandas as pd
import datetime as dt

from instruments import Instruments
import utils
from oanda_api import OandaAPI

#Granularities I want to collect in minutes
INCREMENTS = {
    'M5' : 5,
    'H1' : 60,
    'H4' : 240
}


def create_files(pair, granularity,start_date:str,end_date:str,api):
    #Get about 2000 candles at a time. 
    candle_count = 2000
    #Calculate time
    time_step = INCREMENTS[granularity] * candle_count
    
    end_date = utils.get_utc_dt_from_string(end_date)
    date_from = utils.get_utc_dt_from_string(start_date)

    candle_dfs = []

    date_to = date_from
    while date_to < end_date:
        date_to = date_from + dt.timedelta(minutes=time_step)
        if date_to > end_date:
            date_to = end_date
        
        code, df = api.fetch_candles(pair,
                                            granularity=granularity,
                                            date_from=date_from,
                                            date_to=date_to,
                                            as_df=True)
        if df is not None and df.empty == False:
            candle_dfs.append(df)
        # If issue while collecting data, we will break out of the loop. 
        elif code != 200:
            print("ERROR", pair, granularity,date_from,date_to)
            break
        #Collect Candles
        date_from = date_to
    final_df = pd.concat(candle_dfs)
    final_df.drop_duplicates(subset='time', inplace=True)
    # sort by time in ascending order
    final_df.sort_values(by='time', inplace=True)
    #Save to pickle
    final_df.to_pickle(utils.get_hist_data_filename(pair,granularity))
    #keep track of where i am in the data collection loop
    print(f"{pair}, {granularity}, {final_df.iloc[0].time}, {final_df.iloc[-1].time}")



def run_hist_collection(pair_list, start_date, end_date):
    api = OandaAPI()
    for granularity in INCREMENTS.keys():
        for instrument in Instruments.get_pairs_from_pair_list(pair_list):
            print(granularity,instrument)
            create_files(instrument,granularity,start_date, end_date, api)

if __name__ == "__main__":
    run_hist_collection()