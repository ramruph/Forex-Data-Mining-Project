import pandas as pd
import utils


class Instruments():

    def __init__(self, object):
        self.name = object['name']
        self.type = object['type']
        self.displayName = object['displayName']
        self.piplocation = pow(10, object['pipLocation'])# -4  -> 0.0001 (used for pip differences calculations)
        self.marginRate = object['marginRate']
    
    #representation -> converts to string
    def __repr__(self):
        return str(vars(self))
    
    @classmethod
    def get_instruments_df(cls):
        return pd.read_pickle(utils.get_instrument_data_filename())

    @classmethod
    def get_instruments_list(cls):
        df = cls.get_instruments_df()
        return [Instruments(x) for x in df.to_dict(orient='records')]


    @classmethod
    def get_instruments_dictionary(cls):
        #Dictionary Comprehension
        instruments_list = Instruments.get_instruments_list()

        #List of keys, name property
        instrument_keys = [x.name for x in instruments_list]

        return {key:value for (key,value) in zip(instrument_keys,instruments_list)}

    #Make sure our chosen pair exisits
    @classmethod
    def get_instruments_by_name(cls, pairname):
        dictionary = cls.get_instruments_dictionary()
        if pairname in dictionary:
            return dictionary[pairname]
        else:
            return None
    @classmethod
    def get_pairs_from_pair_list(cls, pair_list):
        existing_pairs = cls.get_instruments_dictionary().keys()
        
        pairs_list = []
        our_currency = pair_list
        for pair in our_currency:
            if pair in existing_pairs:
                pairs_list.append(pair)

        
        return pairs_list



if __name__=="__main__":
    # for key, value in Instruments.get_instruments_dictionary().items():
    #     print(key, value)
    # print(Instruments.get_instruments_by_name('USD_JPY'))
    print(Instruments.get_pairs_from_pair_list(['AUD_USD', 'EUR_USD', 'GBP_USD', 'NZD_USD', 'USD_CAD', 'USD_CHF', 'USD_JPY']))