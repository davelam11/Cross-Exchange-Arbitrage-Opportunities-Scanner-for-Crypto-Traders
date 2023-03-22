import ccxt
import pandas as pd
import datetime
import schedule
import time

# Define exchange instances
binance = ccxt.binance({'apiKey': 'YOUR_API_KEY','secret': 'YOUR_API_SECRET',})
bybit = ccxt.bybit({'apiKey': 'YOUR_API_KEY','secret': 'YOUR_API_SECRET',})
gateio = ccxt.gateio({'apiKey': 'YOUR_API_KEY','secret': 'YOUR_API_SECRET',})
bitfinex = ccxt.bitfinex({'apiKey': 'YOUR_API_KEY','secret': 'YOUR_API_SECRET',})
huobi = ccxt.huobi({'apiKey': 'YOUR_API_KEY','secret': 'YOUR_API_SECRET',})
kucoin = ccxt.kucoin({'apiKey': 'YOUR_API_KEY','secret': 'YOUR_API_SECRET',})

# Define a list of exchange instances
exchange_instances = [binance, bybit, gateio, bitfinex, huobi, kucoin]

# Fetch the list of symbols for each exchange
binance_symbols = binance.load_markets()
bybit_symbols = bybit.load_markets()
gateio_symbols = gateio.load_markets()
bitfinex_symbols = bitfinex.load_markets()
huobi_symbols = huobi.load_markets()
kucoin_symbols = kucoin.load_markets()

def compare_price_differences(exchanges, symbols):
    price_differences = []
    for symbol in symbols:
        symbol_prices = {}
        for exchange in exchanges:
            ticker = exchange.fetch_ticker(symbol)
            symbol_prices[exchange.name] = ticker["last"]
        
        price_differences.append({
            "symbol": symbol,
            "price_difference_percentage": calculate_price_difference_percentage(symbol_prices)
        })
        
    price_differences = sorted(price_differences, key=lambda x: x["price_difference_percentage"], reverse=True)
    return price_differences[:10]

def calculate_price_difference_percentage(symbol_prices):
    price_difference = max(symbol_prices.values()) - min(symbol_prices.values())
    return (price_difference / min(symbol_prices.values())) * 100

def save_data(data):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = f"price_data_{timestamp}.csv"
    df = pd.DataFrame(data)
    df.to_csv(file_name, index=False)

def job():
    top10_price_diff_list = compare_price_differences(exchange_instances, symbols)
    save_data(top10_price_diff_list)

schedule.every(5).minutes.do(job())