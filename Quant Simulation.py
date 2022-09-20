###Please note that the code cannot run as it relies on packages I no longer have access to###

from AmplifyQuantTrading import Data
from AmplifyQuantTrading import Exchange
from AmplifyQuantTrading import MarketMaker
from AmplifyQuantTrading import HedgeFund as hf
from matplotlib import pyplot as plt
from pandas import *
from IPython.display import VimeoVideo

prices = Data.price_series()
price_requests = Data.price_requests()

test_requests = []

for index in range(0, 10): 
    test_requests.append(price_requests[index])
print(test_requests)

request_with_prices = []
for price in prices:
    for request in test_requests:  
        if request[0] == price[0] and request[1] == price[1]:
            request_with_prices.append( (request, price[2]) )
print(request_with_prices)

class QuotedTrade:
    def __init__(self, ticker, trade_volume, ref_price, bid_price, offer_price,
                 date):
        self.ticker = ticker
        self.trade_volume = trade_volume
        self.ref_price = ref_price
        self.bid_price = bid_price
        self.offer_price = offer_price
        self.date = date

    def __str__(self):
        return f'Trade Request for {self.ticker}, {self.trade_volume} shares @ {self.ref_price} on {self.date}. Bid Price: {self.bid_price} and Offer Price: {self.offer_price}'

    def __repr__(self):
        return f'QuotedTrade(ticker={self.ticker}, trade_volume={self.trade_volume}, ref_price={self.ref_price}, bid_price={self.bid_price}, offer_price={self.offer_price}, date={self.date})'

quoted_trades = []
for matched in request_with_prices: 
    bid_price = matched[1] * 0.98 
    offer_price = matched[1] * 1.02 
    quote = QuotedTrade(matched[0][0], matched[0][2], matched[1], bid_price, offer_price, matched[0][1])
    quoted_trades.append(quote)
print(quoted_trades)

hf_responses = []
for trade in quoted_trades:
    response = hf.show(trade) 
    print(response.hf_action)
    hf_responses.append(response)
print(hf_responses)

mm = MarketMaker.mm()
for quote in quoted_trades:
    mm.add_quoted_trade(quote)
print(mm.quoted_trades)

class CompletedTrade:
    def __init__(self, ticker, trade_volume, trade_price, mm_action, ref_price, bid_price, offer_price, date):
        self.ticker = ticker
        self.trade_volume = trade_volume
        self.trade_price = trade_price
        self.mm_action = mm_action 
        self.ref_price = ref_price
        self.bid_price = bid_price
        self.offer_price = offer_price 
        self.date = date

for response in hf_responses: 
    if response.hf_action == "buy":
        mm_action = "sell"
    elif response.hf_action == "sell":
        mm_action = "buy"
    else:
        mm_action = "refuse"
      trade = CompletedTrade(response.ticker, response.trade_volume, response.trade_price, mm_action, response.ref_price, response.bid_price, response.offer_price, response.date)
      mm.add_trade(trade)
print(mm.completed_trades)

bid_data, offer_data, quote_data = [], [], []
for trade in mm.completed_trades:
    if trade.ticker == "AAPL":
        bid_data.append(trade.bid_price)
        offer_data.append(trade.offer_price)
        quote_dates.append(trade.date)
print("bid_data:", bid_data)
print("offer_data:", offer_data)
print("quote_dates:", quote_dates)

ref_data, ref_dates = [], []
for price in prices: 
    if price[0] =="AAPL" and price[1] <= quote_dates[-1]:
        ref_data.append(price[2])
        ref_dates.append(price[1])
print("ref_data:", ref_data)
print("ref_dates:", ref_dates)

axes = plt.subplot() 
axes.plot(quote_dates, bid_data) 
axes.plot(quote_dates, offer_data)
axes.plot(ref_dates, ref_data)

def calculate_spread(quote):
    volume = mm.current_positions[quote[0][0]].position_volume
    if volume > 0:
        bid_price = matched[1] * 0.93 
        offer_price = matched[1] * 1.01 
    elif volume < 0: 
        bid_price = matched[1] * 0.99
        offer_price = matched[1] * 1.07
    else:
        bid_price = matched[1] * 0.98
        offer_price = matched[1] * 1.02
    trade = QuotedTrade(matched[0][0], matched[0][2], matched[1], bid_price, offer_price, matched[0][1])
    quoted_trades.append(trade)
    return trade

def handle_response(trade):
    for response in hf_responses:
        if response.hf_action == "buy":
            mm.action = "sell"
        elif response.hf_action == "sell":
            mm.action = "buy"
        else:
            mm.action == "refuse"
    trade = CompletedTrade(response.ticker, response.trade_volume, response.trade_price, mm_action, response.ref_price, response.bid_price, response.offer_price, response.date)
    mm.add(trade)

for request in price_requests:
    for price in prices:
        if price[0] == request[0] and price[1] == request[1]:
            quote = calculate_spread( (request, price[2]) )
            response = hf.show(quote)
            trade = handle_response(response)







