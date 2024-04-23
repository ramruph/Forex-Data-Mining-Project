import datetime as dt
from dateutil.parser import *

def get_hist_data_filename(pair, granularity):
    return f'historical_data/{pair}_{granularity}.pkl'

def get_instrument_data_filename():
    return 'instruments.pkl'


def time_utc():
    return dt.datetime.now().replace(tzinfo=dt.timezone.utc)

def get_utc_dt_from_string(date_string):
    d = parse(date_string)
    return d.replace(tzinfo=dt.timezone.utc)

if __name__ == "__main__":
    
    print(dt.datetime.now())
    print(time_utc())
    print(get_utc_dt_from_string("2024-02-01 03:00:00"))