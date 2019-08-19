import pandas
import json

def adjclose_json(name):
    str = 'data/excel_files/'+name+'.csv'
    df = pandas.read_csv(str)
    prices = df.drop(["Date","Open", "Low", "High", "Close", "Volume"], axis=1)
    prices = prices.rename(columns = {'Adj Close': 'AdjClose'})
    prices = prices.drop([0])
    adj_close_json = prices.to_json(orient='values')
    return adj_close_json

def adjclose_list(name):
    str = 'data/excel_files/'+name+'.csv' #해당 파일 run시킬때
    #str = 'data/excel_files/'+name+'.csv' #함수 호출시
    df = pandas.read_csv(str)
    prices = df.drop(["Date","Open", "Low", "High", "Close", "Volume"], axis=1)
    prices = prices.drop([0])
    adj_close_list = prices.to_dict(orient='list')
    return adj_close_list

def to_db():
    staples = ['GIS', 'HRL', 'K', 'KHC', 'KO', 'MCD', 'MDLZ', 'MO', 'PEP', 'SBUX', 'STZ', 'WMT']
    giants = ['AAPL', 'AMZN', 'FB', 'GOOG', 'NFLX', 'MSFT']
    # for giant in giants:
    #     Stock.objects.create(ticker=giant, data=adjclose_json(giant))
    # for staple in staples:
    #     Stock.objects.create(ticker=staple, data=adjclose_json(staple))