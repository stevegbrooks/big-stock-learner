# The 'user interface' for our data loading program.

# This script will - when completed - grab data from the API,
# then pkg it up into a .zip. We then manually upload it to AWS S3 bucket (s3://cis545project/data/).
# which will then be the input to the Jupyter notebooks in this repository.

from importlib import reload
import alpha_utils as au
reload(au)

api_key = au.get_alpha_key('secrets.yml')

#get all active listings based as of today
all_active_listings = au.get_alpha_listings(api_key) 
#only need NYSE and NASDAQ...
symbols = all_active_listings[all_active_listings.exchange.isin(['NYSE', 'NASDAQ'])]['symbol'].unique()

#for testing
#symbols = ['IBM', 'MSFT']

#returns a generator, so the calls don't happen until 'join_alpha_results' is called
stock_data = au.yield_alpha_stock_data(
    function = 'TIME_SERIES_DAILY_ADJUSTED',
    symbols = symbols, 
    api_key = api_key,
    data_type = 'csv',
    output_size = 'compact',
    max_threads = 5
)

stock_data = au.join_alpha_results(stock_data, symbols)

stock_data
