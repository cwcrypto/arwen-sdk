__all__ = ['ArwenClient']

import requests
import json

import arwenlib.supportFunctions as sf
from arwenlib.orders import orderDetails, priceInquiry
from arwenlib.baseEscrowDetails import FiltersRequest
from arwenlib.userEscrow import UserEscrowDetails
from arwenlib.exchEscrow import ExchEscrowDetails


class ArwenClient():
    def __init__(self, ip='127.0.0.1', port='5000'):
        self.url = f'http://{ip}:{port}/api/v1'


    def sendRequest(self, endpoint, params = None):

        if(params == None):
            params = dict()

        resp = requests.post(f'{self.url}{endpoint}', json=params).text

        if(resp == None or resp == ''):
            return None

        return  json.loads(resp)


    # Account Management
    def initArwenService(self):
        return requests.post(f'{self.url}/init')


    def pingArwenClient(self):
        return requests.get(f'{self.url}/ping').text


    def timeArwenClient(self):
        return requests.get(f'{self.url}/time').text


    def cleanupBadEscrows(self):
    
        endpoint = '/cleanup'

        return self.sendRequest(endpoint)


    def exchanges(self):

        endpoint = '/exchanges'

        return self.sendRequest(endpoint)


    def registerApiKeys(self, apiKey, apiSecret, exchId='Binonce'):

        endpoint = '/kyc/register'

        reqParams = dict()
        reqParams['exchId'] = exchId
        reqParams['apiKey'] = apiKey
        reqParams['apiSecret'] = apiSecret

        return self.sendRequest(endpoint, reqParams)

    def getOAuthUrl(self, exchId='Binonce'):

        endpoint = '/kyc/oauth'

        reqParams = dict()
        reqParams['exchId'] = exchId

        return self.sendRequest(endpoint, reqParams)

    def getKycStatus(self, exchId='Binonce'):

        endpoint = '/kyc/status'

        reqParams = dict()
        reqParams['exchId'] = exchId

        return self.sendRequest(endpoint, reqParams)


    def feeHistory(self, startTime = None):

        endpoint = '/feehistory'

        reqParams = dict()
        reqParams['startTime'] = startTime

        return self.sendRequest(endpoint, reqParams)

    def getEscrowById(self, escrowType ,escrowId=None):

        if(escrowId == None):
            raise AttributeError('escrowId not set for query by Id')

        if not isinstance(escrowType, sf.EscrowType):
            raise AttributeError('escrowType must be assigned for queryEscrows()')

        escrow = None

        if(escrowType == sf.EscrowType.USER):
            escrow = UserEscrowDetails()
        else:
            escrow = ExchEscrowDetails()
        
        escrowQueryResult = self.queryEscrows(escrowType, escrowId)

        escrow.setFromQuery(escrowQueryResult)

        return escrow

    # Escrow Management
    # Returns list of escrowDetails
    def queryEscrows(
        self,
        escrowType, 
        escrowId = None, 
        startTime = None, 
        isOpen = True, 
        limit = 1000, 
        exchId = None):

        if not isinstance(escrowType, sf.EscrowType):
            raise AttributeError('escrowType must be assigned for queryEscrows()')

        endpoint = f'/{escrowType.value}escrow/query'

        queryParams = FiltersRequest()
        queryParams.setFilter(escrowType, escrowId, startTime, isOpen, limit, exchId)

        escrowList = self.sendRequest(endpoint, queryParams.getFilter())

        if(len(escrowList) == 0):
            return list()

        if(len(escrowList) == 1):
            return escrowList[0]

        return escrowList


    def updateEscrowDetails(self, escrow):
        query = self.queryEscrows(escrow.escrowType, escrow.escrowId)
        escrow.setFromQuery(query)
        return escrow

    # Returns list of escrowIds
    def escrowHistory(self, escrowType, startTime = None):

        endpoint = f'/{sf.EscrowType.value}escrow/history'

        queryParams = dict()
        queryParams['startTime'] = startTime

        escrowIdList = self.sendRequest(endpoint, queryParams)

        return escrowIdList

    # User Escrow Management
    def createNewUserEscrow(
        self,
        reserveAddress,
        exchId = sf.Exchange.BINONCE,
        currency = sf.Blockchain.BTC, 
        expiryTime = sf.generateEscrowTimelock(2.0), 
        qty = 0.025):

        from arwenlib.escrowRequests import NewUserEscrowRequest

        endpoint = '/userescrow/create'

        newUEReq = NewUserEscrowRequest()
        newUEReq.setup(exchId, currency, expiryTime, qty, reserveAddress)

        resp = self.sendRequest(endpoint, newUEReq.getRequest())
        newUEReq.setResponse(resp)

        return newUEReq.createUserEscrowDetails()


    def closeUserEscrow(self, escrow):
        self.closeUserEscrowById(escrow.escrowId)


    def closeUserEscrowById(self, userEscrowId):

        endpoint = '/userescrow/close'

        params = dict()
        params['userEscrowId'] = userEscrowId

        resp = self.sendRequest(endpoint, params)

        return resp['closed']


    # Exchange Escrow Management
    def createNewExchEscrow(
        self,
        reserveAddress,
        userEscrow,
        exchId=sf.Exchange.BINONCE,
        exchEscrowCurrency=sf.Blockchain.LTC,
        qty=2.0,
        expiryTime=sf.generateEscrowTimelock(2.0),
        maxPrice=0.005):
        
        from arwenlib.escrowRequests import NewExchEscrowRequest

        endpoint = '/exchescrow/create'

        newEEReq = NewExchEscrowRequest()
        newEEReq.setup(exchId, exchEscrowCurrency, expiryTime, qty, reserveAddress,
            maxPrice, userEscrow)
        
        resp = self.sendRequest(endpoint, newEEReq.getRequest())
        newEEReq.setResponse(resp)

        return newEEReq.createUserEscrowDetails()


    def priceExchEscrow(
        self,
        exchId=sf.Exchange.BINONCE,
        exchCurrency=sf.Blockchain.LTC,
        qty=2.0,
        expiryTime=sf.generateEscrowTimelock(1.0),
        userCurrency=[sf.Blockchain.BTC, sf.Blockchain.LTC]):
        
        endpoint = '/exchescrow/price'

        params = dict()
        params['exchId'] = exchId.value
        params['exchCurrency'] = exchCurrency.value
        params['qty'] = str(qty)
        params['expiryTime'] = expiryTime
        params['userCurrency'] = [uc.value for uc in userCurrency]

        return self.sendRequest(endpoint, params)


    def closeExchEscrow(self, exchEscrowId):

        endpoint = '/exchescrow/close'

        params = dict()
        params['exchEscrowId'] = exchEscrowId

        resp = self.sendRequest(endpoint, params)

        return resp['closed']


    # Orders
    def ordersHistory(self, startTime = None):

        endpoint = '/orders/history'

        queryParams = dict()
        queryParams['startTime'] = startTime

        orderIdList = self.sendRequest(endpoint, queryParams)

        return orderIdList


    def queryOrderDetailsById(self, orderId):

        order = orderDetails()

        endpoint = '/orders/details'

        params = dict()
        params['orderId'] = order.orderId

        return order.updateFromQuery(self.sendRequest(endpoint, params))


    def queryOrderDetails(self, order):
        return self.queryOrderDetailsById(order.orderId)


    def sellTrade(self, userEscrow, exchEscrow, qty):

        endpoint = '/orders/quote'

        order = orderDetails()
        order.setupOrder(userEscrow, exchEscrow, qty, sf.Side.SELL)
        resp = self.sendRequest(endpoint, order.getRequest())
        order.updateOrderFromQuote(resp)
        
        return order


    def buyTrade(self, userEscrow, exchEscrow, qty):

        endpoint = '/orders/quote'

        order = orderDetails()
        order.setupOrder(userEscrow, exchEscrow, qty, sf.Side.BUY)
        resp = self.sendRequest(endpoint, order.getRequest())
        order.updateOrderFromQuote(resp)
        
        return order


    def inquirePrice(self, userEscrow, exchEscrow, qty, side):

        endpoint = '/orders/inquiry'

        inquiry = priceInquiry(userEscrow, exchEscrow, qty, side)
        resp = self.sendRequest(endpoint, inquiry.getRequest())
        inquiry.setFromInquiry(resp)
        
        return inquiry


    def execute(self, order):

        endpoint = '/orders/execute'
        
        params = dict()
        params['orderId'] = order.orderId

        resp = self.sendRequest(endpoint, params)

        return resp['executed']


    def cancel(self, order):

        endpoint = '/orders/cancel'
        
        params = dict()
        params['orderId'] = order.orderId

        resp = self.sendRequest(endpoint, params)

        return resp['canceled']