import argparse
from finviz.screener import Screener


def get_rsi(data):
    try:
        return float(data['RSI'])
    except:
        return -1

def filter_rsi_under(rsi, x):
    return get_rsi(x) <= float(rsi) and rsi != -1

def filter_rsi_over(rsi, x):
    return get_rsi(x) > float(rsi) and rsi != -1

def print_stock(stock):
    data = {
        'Ticker' : stock['Ticker'],
        'Price' : "$" + str(stock['Price']),
        'RSI' : "RSI: " + str(stock['RSI']),
    }
    
    col_width = max(len(col) for col in data.values()) + 4
    for col in data:
        data[col] = "".join(data[col].ljust(col_width))
        
    print("{ticker} {price} {rsi}".format(ticker = data['Ticker'], price = data['Price'], rsi = data['RSI']))


parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-f', '--filters', type=str, help='FinViz screener filters', default="exch_any cap_mega")
args = parser.parse_args()

#https://finviz.com/screener.ashx?v=121&f=cap_mega&o=-marketcap

# Shows companies which are megacaps ($200 bln or more marketcap)
#filters = ['exch_any', 'cap_mega']
filters = args.filters.split()

# Get the technical table and sort it by marketcap descending
stock_list = Screener(filters=filters, table='Technical', order='-marketcap')


# Print tickers
print("\nTickers:\n")
tickers = [stock['Ticker'] for stock in stock_list]
for a,b,c,d,e in zip(tickers[::5],tickers[1::5],tickers[2::5],tickers[3::5],tickers[4::5]):
    print('{:<20}{:<20}{:<20}{:<20}{:<}'.format(a,b,c,d,e))

# RSI
stock_list_by_rsi = sorted(stock_list.data, key=get_rsi)
stock_list_by_rsi_rev = sorted(stock_list.data, key=get_rsi, reverse=True)

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
    rsi_lists['data']['under'][rsi] = list(filter(lambda x : filter_rsi_under(rsi, x), stock_list_by_rsi))

for rsi in rsi_lists['values']['above']:
    rsi_lists['data']['above'][rsi] = list(filter(lambda x : filter_rsi_over(rsi, x), stock_list_by_rsi))

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
