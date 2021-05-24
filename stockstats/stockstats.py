import argparse
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries

# Set your API key
ALPHA_VANTAGE_API_KEY = "YOUR_API_KEY_HERE"

ts = TimeSeries(key=ALPHA_VANTAGE_API_KEY)
ti = TechIndicators(key=ALPHA_VANTAGE_API_KEY, output_format='json')

parser = argparse.ArgumentParser()
parser.add_argument("symbols", nargs='+')
args = parser.parse_args()

for symbol in args.symbols:
    symbol = symbol.upper()
    
    try:
        # get current price
        data, meta_data = ts.get_intraday(symbol)
        current_price = list(data.values())[0]
        current_price = (float(current_price['2. high']) + float(current_price['3. low'])) / 2

        # get first band
        data, meta_data = ti.get_bbands(symbol=symbol, interval='daily', time_period=60)
        first_band = list(data.values())[0]

        current = float(current_price)
        lower = float(first_band['Real Lower Band'])
        mid = float(first_band['Real Middle Band'])
        upper = float(first_band['Real Upper Band'])
        
        percent_lower_current = round(((lower - current) / current) * 100, 2)
        percent_mid_current = round(((mid - current) / current) * 100, 2)
        percent_upper_current = round(((upper - current) / current) * 100, 2)
        
        display = "{0}: Current: {1:.2f} Bands: {2:.2f} ({3:+.2f}%), {4:.2f} ({5:+.2f}%), {6:.2f} ({7:+.2f}%)".format(symbol, current, lower, percent_lower_current, mid, percent_mid_current, upper, percent_upper_current)
        print(display)
        
        percent_lower_current_abs = abs(percent_lower_current)
        percent_mid_current_abs = abs(percent_mid_current)
        percent_upper_current_abs = abs(percent_upper_current)
        
        if percent_lower_current_abs <= 3:
            print("Within 3% of lower band!")
        
    except:
        print("{0}: Error fetching data".format(symbol))

