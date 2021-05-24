from operator import itemgetter
from finviz.screener import Screener

#https://finviz.com/screener.ashx?v=121&f=cap_mega&o=-marketcap

# Shows companies which are megacaps ($200 bln or more marketcap)
filters = ['exch_any', 'cap_mega']

# Get the technical table and sort it by marketcap descending
stock_list = Screener(filters=filters, table='Technical', order='-marketcap')

# Print tickers
print("\nTop 200 Billion Plus Market Cap Companies:")
tickers = [stock['Ticker'] for stock in stock_list]
for a,b,c,d,e in zip(tickers[::5],tickers[1::5],tickers[2::5],tickers[3::5],tickers[4::5]):
    print('{:<20}{:<20}{:<20}{:<20}{:<}'.format(a,b,c,d,e))

# RSI
stock_list_by_rsi = sorted(stock_list.data, key=lambda x: float(x['RSI']))
stock_list_rsi_under_50 = list(filter(lambda x : float(x['RSI']) < 50, stock_list_by_rsi))

print("\nRSI under 50:")
for stock in stock_list_rsi_under_50:
    print("${ticker} ${price} RSI: {rsi}".format(ticker = stock['Ticker'], price = stock['Price'], rsi = stock['RSI']))
print()
