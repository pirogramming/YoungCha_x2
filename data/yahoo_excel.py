import pandas
import json

def data_adjclose(name):
    str = 'excel_files/'+name+'.csv'
    df = pandas.read_csv(str)
    prices = df.drop(["Open", "Low", "High", "Close", "Volume"], axis=1)
    prices = prices.drop([0])
    adj_close_json = prices.to_json(orient='records')
    return adj_close_json

staples = ['GIS','HRL','K','KHC','KO','MCD','MDLZ','MO','PEP','SBUX','STZ','WMT']
giants = ['AAPL','AMZN','FB','GOOG','FB','MSFT']
for staple in staples:
    print(data_adjclose(staple))
for giant in giants:
    print(data_adjclose(giant))