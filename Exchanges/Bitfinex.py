#!/usr/bin/env python3

import requests
from urllib.parse import urlencode, urljoin, urlparse


BITFINEX_API_URL = 'https://api.bitfinex.com/'
BITFINEX_API_VERSION = 'v1/'
BITFINEX_GETSYMBOLS_URL = 'symbols'
BITFINEX_GETTICKER_URL = 'pubticker/{}'
BITFINEX_GETSTATS_URL = 'stats/{}'
BITFINEX_GETFUNDINGBOOK_URL = 'lendbook/{}?limit_bids={}&limit_asks={}'
BITFINEX_GETORDERBOOK_URL = 'book/{}?limit_bids={}&limit_asks={}&group={}'
BITFINEX_GETTRADES_URL = 'trades/{}?limit_trades={}&timestamp={}'
BITFINEX_GETLENDS_URL = 'lends/{}?limit_lends={}&timestamp={}'
BITFINEX_GETSYMBOLSDETAILS_URL = 'symbols_details'


class Bitfinex():
  def __init__(self, apiKey=None, apiSecret=None):
    self.apiKey = apiKey
    self.apiSecret = apiSecret
    self.apiUrl = urljoin(BITFINEX_API_URL, BITFINEX_API_VERSION)


  def query(self, basicUrl, private=False):
    url = urljoin(self.apiUrl, basicUrl)

    try: 
      data = requests.get(url).json()
      data = {'success': True, 'message': '', 'results': data}
    except:
      data = {'success': False, 'message': 'Comunication error'}

    return data


  def getTicker(self, market):
    return self.query(BITFINEX_GETTICKER_URL.format(market))
  
  def getStats(self, market):
    return self.query(BITFINEX_GETSTATS_URL.format(market))

  def getOrderBook(self, market, limitBids=50 , limitAsks=50, group=1):
    return self.query(BITFINEX_GETORDERBOOK_URL.format(market, limitBids, limitAsks, group))

  def getLends(self, currency, limitLends=50, timestamp=''):
    return self.query(BITFINEX_GETLENDS_URL.format(currency, limitLends, timestamp))

  def getFundingBook(self, currency, limitBids=50, limitAsks=50):
    return self.query(BITFINEX_GETFUNDINGBOOK_URL.format(currency, limitBids, limitAsks))

  def getTrades(self, market, limitTrades=50, timestamp=''):
    return self.query(BITFINEX_GETTRADES_URL.format(market, limitTrades, timestamp))

  def getSymbols(self):
    return self.query(BITFINEX_GETSYMBOLS_URL)

  def getSymbolsDetails(self):
    return self.query(BITFINEX_GETSYMBOLSDETAILS_URL)
  