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

rsi_lists = {
    'values': {
        'under' : ['50', '45', '40', '35'],
        'above' : ['70', '60', '50']
    },
    'data': {
        'under' : dict(),
        'above' : dict()
    },
}

for rsi in rsi_lists['values']['under']:
    rsi_lists['data']['under'][rsi] = list(filter(lambda x : float(x['RSI']) < float(rsi), stock_list_by_rsi))

for rsi in rsi_lists['values']['above']:
    rsi_lists['data']['above'][rsi] = list(filter(lambda x : float(x['RSI']) > float(rsi), stock_list_by_rsi))

rsi_list_types = ['under', 'above']
for type in rsi_list_types:
    for rsi in rsi_lists['values'][type]:
        print("\nRSI {type} {rsi}:\n".format(type = type, rsi = rsi))
        for stock in rsi_lists['data'][type][rsi]:
            print_stock(stock)


# consider buying/selling
tickers_rsi_under_45 = [stock['Ticker'] for stock in rsi_lists['data']['under']['45']]
tickers_rsi_above_60 = [stock['Ticker'] for stock in rsi_lists['data']['above']['60']]

print("\nConsider buying (RSI under 45): {}".format(", ".join(tickers_rsi_under_45)))
print("\nConsider selling (RSI above 60): {}".format(", ".join(tickers_rsi_above_60)))

# blank line at end
print()
