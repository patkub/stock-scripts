from operator import itemgetter
from finviz.screener import Screener

def print_stock(stock):
    print("{ticker} \t ${price} \t RSI: {rsi}".format(ticker = stock['Ticker'], price = stock['Price'], rsi = stock['RSI']))

#https://finviz.com/screener.ashx?v=121&f=cap_mega&o=-marketcap

# Shows companies which are megacaps ($200 bln or more marketcap)
filters = ['exch_any', 'cap_mega']

# Get the technical table and sort it by marketcap descending
stock_list = Screener(filters=filters, table='Technical', order='-marketcap')

# Print tickers
print("\nTop 200 Billion Plus Market Cap Companies:\n")
tickers = [stock['Ticker'] for stock in stock_list]
for a,b,c,d,e in zip(tickers[::5],tickers[1::5],tickers[2::5],tickers[3::5],tickers[4::5]):
    print('{:<20}{:<20}{:<20}{:<20}{:<}'.format(a,b,c,d,e))

# RSI
stock_list_by_rsi = sorted(stock_list.data, key=lambda x: float(x['RSI']))
stock_list_by_rsi_rev = sorted(stock_list.data, key=lambda x: float(x['RSI']), reverse=True)
stock_list_rsi_under = dict()
rsi_under_list = ['50', '45', '40', '35']

for rsi in rsi_under_list:
    stock_list_rsi_under[rsi] = list(filter(lambda x : float(x['RSI']) < float(rsi), stock_list_by_rsi))

for rsi in rsi_under_list:
    print("\nRSI under {rsi}:\n".format(rsi = rsi))
    for stock in stock_list_rsi_under[rsi]:
        print_stock(stock)

stock_list_rsi_above_60 = list(filter(lambda x : float(x['RSI']) > float(60), stock_list_by_rsi_rev))

print("\nRSI above 60:\n")
for stock in stock_list_rsi_above_60:
    print_stock(stock)

# blank line at end
print()
