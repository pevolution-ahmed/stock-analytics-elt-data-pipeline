from pandas_datareader import data as pd_reader
import datetime as dt
from pandas import DataFrame 
from google.oauth2 import service_account

def _save_stocks_data_to_gbq(ticker, syear, smonth, sday, eyear, emonth, eday,sa_path):
    start = dt.datetime(syear, smonth, sday)
    end = dt.datetime(eyear, emonth, eday)
    df = pd_reader.DataReader(ticker, 'yahoo', start, end)
    credentials = service_account.Credentials.from_service_account_file(sa_path)
    df.rename(columns = {'Adj Close':'Adj_Close'}, inplace = True)
    df.reset_index(inplace=True)
    df.to_gbq(
        destination_table='stocks_storage.stocks_data',
        project_id='stocks-analytics-361812',
        credentials=credentials,
        if_exists= 'replace'
    )
