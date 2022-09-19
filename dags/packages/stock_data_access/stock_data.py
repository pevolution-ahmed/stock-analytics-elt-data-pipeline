from pandas_datareader import data as pd_reader
import datetime as dt
import pandas as pd
from google.oauth2 import service_account

def _save_stocks_data_to_gbq(tickers, syear, smonth, sday, eyear, emonth, eday,sa_path):
    start = dt.datetime(syear, smonth, sday)
    end = dt.datetime(eyear, emonth, eday)
    credentials = service_account.Credentials.from_service_account_file(sa_path)

    stock_list = [pd_reader.DataReader(t, 'yahoo', start, end) for t in tickers]
    mult_df = pd.concat(stock_list,keys=tickers).reset_index().rename(columns = {'level_0':'Stock'})
    mult_df.rename(columns = {'Adj Close':'Adj_Close'}, inplace = True)
    mult_df.to_gbq(
        destination_table='stocks_storage.stocks_data',
        project_id='stocks-analytics-361812',
        credentials=credentials,
        if_exists= 'replace'
    )
