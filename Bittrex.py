#!/usr/bin/env python3

import requests
import time
import base64
import hmac
import hashlib
import json
from urllib.parse import urlencode, urljoin, urlparse

BITTREX_API_URL = 'https://bittrex.com/api/'
BITTREX_API_VERSION = 'v1.1/'
BITTREX_GETCURRENCIES_URL = 'public/getcurrencies'
BITTREX_GETMARKETHISTORY_URL = 'public/getmarkethistory?market={}'
BITTREX_GETMARKETS_URL = 'public/getmarkets'
BITTREX_GETMARKETSUMMARIES_URL = 'public/getmarketsummaries'
BITTREX_GETMARKETSUMMARY_URL = 'public/getmarketsummary?market={}'
BITTREX_GETORDERBOOK_URL = 'public/getorderbook?market={}&type={}'
BITTREX_GETTICKER_URL = 'public/getticker?market={}'
BITTREX_GETWITHDRAWALHISTORY_URL = 'account/getwithdrawalhistory?currency={}'
BITTREX_GETBALANCE_URL = 'account/getbalance?currency={}'
BITTREX_GETBALANCES_URL = 'account/getbalances'
BITTREX_GETDEPOSITADDRESS_URL = 'account/getdepositaddress?currency={}'
BITTREX_GETDEPOSITHISTORY_URL = 'account/getdeposithistory?currency={}'
BITTREX_GETOPENORDERS_URL = 'market/getopenorders?market={}'
BITTREX_GETORDER_URL = 'account/getorder?uuid={}'
BITTREX_GETORDERHISTORY_URL = 'account/getorderhistory?market={}'
BITTREX_SETACCOUNTWITHDRAW_URL = 'account/withdraw?currency={}&quantity={}&address={}'
BITTREX_SETBUYLIMIT_URL = 'market/buylimit?market={}&quantity={}&rate={}'
BITTREX_SETCANCEL_URL = 'market/cancel?&uuid={}'
BITTREX_SETSELLLIMIT_URL = 'market/selllimit?market={}&quantity={}&rate={}'

class Bittrex():
  def __init__(self, apiKey=None, apiSecret=None):
    self.apiKey = apiKey
    self.apiSecret = apiSecret
    self.apiUrl = urljoin(BITTREX_API_URL, BITTREX_API_VERSION)

  def query(self, basicUrl, private=False):
    url = urljoin(self.apiUrl, basicUrl)
    headers = {}
    if private:
      nonce = str(int(time.time() * 1000))
      url += ('&' if urlparse(url).query else '?') + urlencode({'apikey': self.apiKey, 'nonce': nonce})
      apisign = hmac.new(self.apiSecret.encode(), url.encode(), hashlib.sha512).hexdigest()
      headers['apisign'] = apisign
      
    try:
      data = requests.get(url, headers=headers).json()
    except:
      data = {'success': False, 'message': 'Comunication error'}

    return data


  #
  #Public
  #
  def getCurrencies(self):
    return self.query(BITTREX_GETCURRENCIES_URL)

  def getMarketHistory(self, market):
    return self.query(BITTREX_GETMARKETHISTORY_URL.format(market))

  def getMarkets(self):
    return self.query(BITTREX_GETMARKETS_URL)

  def getMarketSummaries(self):
    return self.query(BITTREX_GETMARKETSUMMARIES_URL)

  def getMarketSummary(self, market):
    return self.query(BITTREX_GETMARKETSUMMARY_URL.format(market))

  def getOrderBook(self, market, type='both'):
    return self.query(BITTREX_GETORDERBOOK_URL.format(market, type))

  def getTicker(self, market):
    return self.query(BITTREX_GETTICKER_URL.format(market))

  #
  #Private
  #
  def getAccountWithdrawHistory(self, currency):
    return self.query(BITTREX_GETWITHDRAWALHISTORY_URL.format(currency), private=True)

  def getBalance(self, currency):
    return self.query(BITTREX_GETBALANCE_URL.format(currency), private=True)

  def getBalances(self):
    return self.query(BITTREX_GETBALANCES_URL, private=True)

  def getDepositAddress(self, currency):
    return self.query(BITTREX_GETDEPOSITADDRESS_URL.format(currency), private=True)

  def getDepositHistory(self, currency):
    return self.query(BITTREX_GETDEPOSITHISTORY_URL.format(currency), private=True)

  def getOpenOrders(self, market=''):
    return self.query(BITTREX_GETOPENORDERS_URL.format(market), private=True)
  
  def getOrder(self, uuid):
    return self.queery(BITTREX_GETORDER_URL.format(uuid), private=True)

  def getOrderHistory(self, market):
    return self.query(BITTREX_GETORDERHISTORY_URL.format(market), private=True)

  def setAccountWithdraw(self, currency, quantity, address):
    return self.query(BITTREX_SETACCOUNTWITHDRAW_URL.format(currency, quantity, address), private=True)

  def setBuyLimit(self, market, quantity, rate):
    return self.query(BITTREX_SETBUYLIMIT_URL.format(market, quantity, rate), private=True)

  def setCancel(self, orderUuid):
    return self.query(BITTREX_SETCANCEL_URL.format(orderUuid), private=True)

  def setSellLimit(self, market, quantity, rate):
    return self.query(BITTREX_SETSELLLIMIT_URL.format(market, quantity, rate), private=True)
