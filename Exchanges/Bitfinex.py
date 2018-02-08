#!/usr/bin/env python3

import requests
import hashlib
import time
import hmac
import json
import base64
from urllib.parse import urlencode, urljoin, urlparse


BITFINEX_API_URL = 'https://api.bitfinex.com/'
BITFINEX_API_VERSION = 'v1/'
BITFINEX_GETACCOUNTINFOS_URL = 'account_infos'
BITFINEX_GETACCOUNTFEES_URL = 'account_fees'
BITFINEX_GETSUMMARY_URL = 'summary'
BITFINEX_GETDEPOSITNEW_URL = 'deposit/new'
BITFINEX_GETKEYINFO_URL = 'key_info'
BITFINEX_GETMARGININFOS_URL = 'margin_infos'
BITFINEX_GETBALANCES_URL = 'balances'
BITFINEX_GETTRANSFERBETWEENWALLETS_URL = 'transfer'
BITFINEX_SETWITHDRAWL_URL = 'withdraw'
BITFINEX_SETORDERNEW_URL = 'order/new'
BITFINEX_SETORDERSNEW_URL = 'order/new/multi'
BITFINEX_SETORDERCANCEL_URL = 'order/cancel'
BITFINEX_SETORDERSCANCEL_URL = 'order/cancel/multi'
BITFINEX_SETORDERCANCELALL_URL = 'order/cancel/all'
BITFINEX_SETORDERREPLACE_URL = 'order/cancel/replace'
BITFINEX_GETORDERSTATUS_URL = 'order/status'
BITFINEX_GETORDERSACTIVE_URL = 'orders'
BITFINEX_GETORDERSHISTORY_URL = 'orders/hist'
BITFINEX_GETPOSITIONSACTIVE_URL = 'positions'
BITFINEX_SETPOSITIONCLAIM_URL = 'positions/claim'
BITFINEX_GETBALANCEHISTORY_URL = 'history'
BITFINEX_GETDEPOSITWITHDRAWALHISTORY_URL = 'history/movements'
BITFINEX_GETTRADESHISTORY_URL = 'mytrades'
BITFINEX_SETOFFERNEW_URL = 'offer/new'
BITFINEX_SETOFFERCANCEL_URL = 'offer/cancel'
BITFINEX_GETOFFERSTATUS_URL = 'offer/status'
BITFINEX_GETCREDITSACTIVE_URL = 'credits'
BITFINEX_GETOFFERS_URL = 'offers'
BITFINEX_GETOFFERHISTORY_URL = 'offers/hist'
BITFINEX_GETTRADESPASTFUNDING_URL = 'mytrades_funding'
BITFINEX_GETFUNDINGACTIVE_URL = 'taken_funds'  #active funding used in a margin position
BITFINEX_GETFUNDINGACTIVEUNUSED_URL = 'unused/taken/funds'  #active funding not used in a margin position
BITFINEX_GETFUNDSTOTAL_URL = 'total_taken_funds'
BITFINEX_SETCLOSEDMARGINFUNDING_URL = 'funding/close'
BITFINEX_SETBASKETMANAGE_URL = 'basket_manage'
BITFINEX_SETPOSITIONSCLOSE_URL = 'positions/close'
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


  def query(self, path, private=False, data={}):
    url = urljoin(self.apiUrl, path)
    
    if private:
      headers = {}
      nonce = str(int(time.time() * 1000))
      body = {'request': '/'+BITFINEX_API_VERSION+path, 'nonce': nonce}
      body.update(data)
      payload = base64.b64encode(json.dumps(body).encode())
      apisign = hmac.new(self.apiSecret.encode(), payload, hashlib.sha384).hexdigest()

      headers['X-BFX-APIKEY'] = self.apiKey
      headers['X-BFX-PAYLOAD'] = payload
      headers['X-BFX-SIGNATURE'] = apisign

#      if private:
#        res = requests.post(url, headers=headers, data=body)
#      else: 
#        res = requests.get(url)

    try:
      if private:
        res = requests.post(url, headers=headers, data=body)
      else: 
        res = requests.get(url)
      res = {'success': True, 'message': '', 'results': res.json()}
    except:
      res = {'success': False, 'message': 'Comunication error'}

    return res

  #
  #Public
  #
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
  
  #
  #Private
  #
  def getAccountInfos(self):
    return self.query(BITFINEX_GETACCOUNTINFOS_URL, private=True)

  def getAccountFees(self):
    return self.query(BITFINEX_GETACCOUNTFEES_URL, private=True)

  def getSummary(self):
    return self.query(BITFINEX_GETSUMMARY_URL, private=True)

  def getDeposit(self, method='bitcoin', walletName='exchange', renew=1):
    return self.query(BITFINEX_GETDEPOSITNEW_URL, private=True, data={'method': method, 'wallet_name': walletName, 'renew': renew})

  def getKeyInfo(self):
    return self.query(BITFINEX_GETKEYINFO_URL, private=True)

  def getMarginInformation(self):
    return self.query(BITFINEX_GETMARGININFOS_URL, private=True)
    
  def getWalletBalances(self):
    return self.query(BITFINEX_GETBALANCES_URL, private=True)

  def setTransferBetweenWallets(self, amount=0, currency=None, walletFrom=None, walletTo=None):
    return self.query(BITFINEX_GETTRANSFERBETWEENWALLETS_URL, private=True, data={'amount': amount, 'currency': , 'walletfrom': walletFrom, 'walletto': walletTo})

  def setWithdrawl(self, withdrawType=None, walletSelected=None, amount=0, address= None):
    return self.query(BITFINEX_SETWITHDRAWL_URL, private=True, data={'withdraw_type': withdrawType, 'walletselected': walletSelected, 'amount': amount, 'address': address})
    
  def setNewOrder(self, symbol=None, amount=0, price=0, exchange=None, side=None, type=None):
    return self.uery(BITFINEX_SETORDERNEW_URL, private=True, data={'symbol': symbol, 'amount': amount, 'price': price, 'exchange': exchange, 'side': side, 'type': type})

  def setNewOrders(self, orders=[]):
    return self.query(BITFINEX_SETORDERSNEW_URL, private=True, data=orders)

  def setCancelOrder(self, id=None):
    return self.query(BITFINEX_SETORDERCANCEL_URL, private=True, data={'id': id})

  def setCancelOrders(selfm, ids=[]):
    return self.query(BITFINEX_SETORDERSCANCEL_URL, private=True, data={'ids': ids})

  def setCancelAllOrders(self):
    return self.query(BITFINEX_SETORDERCANCELALL_URL, private=True)

  def setReplaceOrder(self, id=None, symbol=None, amount=0, price=0, exchange=None, side=None, type=None):
    return self.query(BITFINEX_SETORDERREPLACE_URL, private=True, data={'id': id, 'symbol': symbol, 'amount': amount, 'price': price, 'exchange': exchange, 'side': side, 'type': type})

  def getOrderStatus(self, id=None):
    return self.query(BITFINEX_GETORDERSTATUS_URL, private=True, data={'id': id})

  def getActiveOrders(self):
    return self.query(BITFINEX_GETORDERSACTIVE_URL, private=True)

  def getOrderHistory(self):
    return self.query(BITFINEX_GETORDERSHISTORY_URL, private=True)

  def getActivePositions(self):
    return self.query(BITFINEX_GETPOSITIONSACTIVE_URL, private=True)

  def setClaimPosition(self, id=None, amount=0):
    return self.query(BITFINEX_SETPOSITIONCLAIM_URL, private=True data={'id': id, 'amount': amount})

  def getBalanceHistory(self, currency=None):
    return self.query(BITFINEX_GETBALANCEHISTORY_URL, private=True data={'currency': currency})

  def getDepositWithdrawalHistory(self, currency=None):
    return self.query(BITFINEX_GETDEPOSITWITHDRAWALHISTORY_URL, private=True, data={'currency': currency})

  def getPastTrades(self, currency=None):
    return self.query(BITFINEX_GETTRADESHISTORY_URL, private=True, data={'currency': currency})

  def setNewOrder(self, currency=None, amount=0, rate=0, period=0, direction=None):
    return self.query(BITFINEX_SETORDERNEW_URL, private=True, data={'currency': currency, 'amount': amount, 'rate': rate, 'period': period, 'direction': direction})

  def setCancelOrder(self, offerId=None):
    return self.query(BITFINEX_SETORDERCANCEL_URL, private=True, data={'offer_id': id})

  def getOrderStatus(self, orderId=None):
    return self.query(BITFINEX_GETOFFERSTATUS_URL, private=True, data={'offer_id': offerId})

  def getActiveCredits(self):
    return self.query(BITFINEX_GETCREDITSACTIVE_URL, private=True)

  def getOffers(self):
    return self.query(BITFINEX_GETOFFERS_URL, private=True)

  def getOffersHistory(self):
    return self.query(BITFINEX_GETOFFERHISTORY_URL, private=True)

  def getPastFundingTrades(self, symbol=None):
    return self.query(BITFINEX_GETTRADESPASTFUNDING_URL, private=True, data={'symbol': symbol})

  def getActiveFundingUsedInMarginPosition(self):
    return self.query(BITFINEX_GETFUNDINGACTIVE_URL, private=True)

  def getActiveFundingNoyUsedInMarginPosition(self):
    return self.query(BITFINEX_GETFUNDINGACTIVEUNUSED_URL, private=True)

  def getTotalTakenFunds(self):
    return self.query(BITFINEX_GETFUNDSTOTAL_URL private=True)

  def setCloseMarginFunding(self, swapId=None):
    return self.query(BITFINEX_SETCLOSEDMARGINFUNDING_URL, private=True, data={'swap_Id': swapId})

  def setBasketManage(self, amount=0, dir=0, name='btc_btu'):
    return self.query(BITFINEX_SETBASKETMANAGE_URL, private=True, data={'amount': amount,'dir': dir, 'name': name})

  def setClosePosition(self, id=None):
    return self.query(BITFINEX_SETPOSITIONSCLOSE_URL, private=True, data={'id': id})

