import robin_stocks.robinhood as r
import time
import pyotp
import sys
import math 

totp = pyotp.TOTP("GTGBTO63C46YCH65").now()
login = r.login("dnathunder@gmail.com", "Khazanchi2021!", mfa_code=totp)

def truncate(number, decimals=0):
    """
    Returns a value truncated to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer.")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more.")
    elif decimals == 0:
        return math.trunc(number)

    factor = 10.0 ** decimals
    return math.trunc(number * factor) / factor

# GETTERS 

def get_price(ticker):
   tick = r.get_latest_price(ticker)
   return float(tick[0])

def get_current_holdings(): # returns all holdings as dictionary
   return r.build_holdings()


# SELL WRAPPERS
# additional argument, either gtc (good till cancelled), 
# gfd (good for day), or ioc (immediate or cancel). Currently IOC

# Sells a stock by quantity
def sell(ticker, amount):
   purchase = r.order_sell_market(ticker, amount)
   print(purchase)

# Sells a stock by price
def sell_market_by_price(ticker, amount, isCrypto):
   if not isCrypto:
      r.order_sell_fractional_by_price(ticker, amount)
   else:
      r.order_sell_crypto_by_price(ticker, amount)
   
   print("Executed sell by price order")
   
# Sells all of a stock currently possessed, returns price of sale
def sell_all(ticker, isCrypto):
   print("Sold all of: " + ticker)

# Sells stock once it hits a certain limit price
# price in this case refers to the price of 1 stock at 
# whatever price limit you want
def sell_at_certain_price(ticker, amount, price, isCrypto):
   if not isCrypto:
      r.order_sell_limit(ticker, amount, price)
   else:
      r.order_sell_crypto_limit(ticker, amount, price)
   
   print("sold at limit purchase order")



# PURCHASE WRAPPERS
# additional argument, either gtc (good till cancelled), 
# gfd (good for day), or ioc (immediate or cancel). Currently IOC

# Purchases a stock by quantity
def buy(ticker, amount, isCrypto):
   if not isCrypto:
      purchase = r.order_buy_market(ticker, amount)
   else:
      purchase = r.order_buy_crypto_by_quantity(ticker, amount)
   
   print("Executed purchase order by quantity")

# Buys a stock by price 
def buy_market_by_price(ticker, price, isCrypto):
   if not isCrypto:
      purchase = r.orders.order_buy_fractional_by_price(ticker, price, timeInForce='gtc')
      print("Executed price purchase order regular")
   else:
      purchase = r.order_buy_crypto_by_price(ticker, price)
      print("Executed price purchase order crypto")
   
# Buys a stock when it hits a certain price point
# price in this case refers to the price of 1 stock at 
# whatever price limit you want
def buy_at_certain_price(ticker, amount, price, isCrypto):
   if not isCrypto:
      r.orders.order_buy_limit(ticker, amount, price)
   else:
      r.orders.order_buy_crypto_limit(ticker, amount, price)

   print("Executed limit order")


# EXECUTION FUNCTIONALITY

# Function is repeatedly called by 
# main. Upon termination, it will cease all trading
def run(stock='btc', crypto=True): 
   print('PURCHASING')
   buy_market_by_price(stock, 20, crypto)

   # bought price of stock
   bought_price = round(float(r.orders.get_all_crypto_orders(info=None)[0]['price']), 0)
   # our limit
   limit_price = bought_price * 1.04
   # how much we bought
   quantity = float(r.orders.get_all_crypto_orders(info=None)[0]['quantity'])

   time.sleep(5)
   sell_at_certain_price(stock, quantity, limit_price, crypto)
   print("sent limit order")


if __name__ == "__main__":
   run()
   # while True:
   #    prev_order = r.orders.get_all_crypto_orders(info=None)[0]['side']
   #    prev_order_state = r.orders.get_all_crypto_orders(info=None)[0]['state']
   
   #    print(r.orders.get_all_crypto_orders(info=None)[0])

   #    if prev_order == 'sell' and prev_order_state == 'filled':
   #       run()
      
   #    print("print me plz")
   #    time.sleep(1)