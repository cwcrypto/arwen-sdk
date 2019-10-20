__all__ = ['ArwenClient']

import sys

if sys.version_info[0] != 3 or sys.version_info[1] != 6 or sys.version_info[2] != 8:
    print("This script requires Python version 3.6.8")
    sys.exit(1)

import requests
import json

from . import supportFunctions as sf
from .orders import OrderDetails
from .baseEscrowDetails import FiltersRequest, EscrowDetails
from .userEscrow import UserEscrowDetails
from .exchEscrow import ExchEscrowDetails
from .messages import baseResponse, apiRequests, apiResponses
from .exceptions import ProtocolException, SystemException

from typing import Type, cast, TypeVar

class ArwenClient():
    url: str

    def __init__(self, ip, port):
        self.url = f'http://{ip}:{port}/api/v1'


    def sendRequest(self, endpoint, params = None):

        if(params == None):
            params = dict()

        resp = requests.post(f'{self.url}{endpoint}', json=params).text

        if(resp == None or resp == ''):
            return None

        parsedResp = baseResponse.api_base_response_from_dict(json.loads(resp))

        if(parsedResp.code == 500):
            raise ProtocolException(parsedResp.error, parsedResp.data)
        
        if(parsedResp.code == 400):
            raise SystemException(parsedResp.error, parsedResp.data)

        return json.loads(parsedResp.data)
        

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


    def registerApiKeys(self, apiKey, apiSecret, exchId: sf.Exchange):

        endpoint = '/kyc/register'

        requestObj = apiRequests.APIRegisterKeys(exchId.value, apiKey, apiSecret)
        response = self.sendRequest(endpoint, requestObj.to_dict())

        return apiResponses.api_key_reg_response_from_dict(response)

    def getOAuthUrl(self, exchId: sf.Exchange):

        endpoint = '/kyc/oauth'

        requestObj = apiRequests.APIOuathRequest(exchId.value)
        response = self.sendRequest(endpoint, requestObj.to_dict())

        return apiResponses.api_ouath_response_from_dict(response)

    def getKycStatus(self, exchId: sf.Exchange):

        endpoint = '/kyc/status'

        requestObj = apiRequests.APIKYCStatusRequest(exchId.value)
        response = self.sendRequest(endpoint, requestObj.to_dict())

        return apiResponses.api_kyc_status_response(response)
    

    def queryEscrowById(self, escrowType: sf.EscrowType, escrowId: str) -> EscrowDetails:

        if(escrowId == None or escrowId == ""):
            raise AttributeError('escrowId not set for query by Id')

        if not isinstance(escrowType, sf.EscrowType):
            raise AttributeError('escrowType must be assigned for queryEscrows()')

        responseObj = self.queryEscrows(escrowType, escrowId)

        if(escrowType == sf.EscrowType.USER):
            escrow = UserEscrowDetails()
        else:
            escrow = ExchEscrowDetails()
            
        escrow.setFromQuery(responseObj[0])

        return escrow

    # Escrow Management
    # Returns list of escrowDetails
    def queryEscrows(
        self,
        escrowType, 
        escrowId = None, 
        fromTime = None, 
        isOpen = True, 
        limit = 1000, 
        exchId = None) -> list():

        if not isinstance(escrowType, sf.EscrowType):
            raise AttributeError('escrowType must be assigned for queryEscrows()')

        endpoint = f'/{escrowType.value}escrow/query'

        queryParams = apiRequests.APIFilterRequest(escrowId, fromTime, limit, exchId, not isOpen)

        response = self.sendRequest(endpoint, queryParams.to_dict)
        responseObj = None

        if(escrowType == sf.EscrowType.USER):
            responseObj = apiResponses.api_user_escrow_from_dict(response)
        else:
            responseObj = apiResponses.api_exchange_escrow_from_dict(response)

        if(len(responseObj) == 0):
            return None

        return responseObj


    def updateExchangeEscrow(self, escrow: apiResponses.APIExchangeEscrowElement) -> ExchEscrowDetails:
        return self.queryEscrowById(sf.EscrowType.EXCH, escrow.exch_escrow_id)
    
    def updateUserEscrow(self, escrow: apiResponses.APIExchangeEscrowElement) -> UserEscrowDetails:
        return self.queryEscrowById(sf.EscrowType.USER, escrow.exch_escrow_id)


    # User Escrow Management
    def createNewUserEscrow(
        self,
        reserveAddress: str,
        exchId: str,
        currency: sf.Blockchain, 
        expiryTime: int, 
        amount: float) -> UserEscrowDetails:

        endpoint = '/userescrow/create'

        newUserEscrowRequest = apiRequests.APINewUserEscrowRequest(exchId, currency, amount, reserveAddress, expiryTime)

        response = self.sendRequest(endpoint, newUserEscrowRequest.to_dict())
        responseObj = apiResponses.api_new_user_escrow_response_from_dict(response)

        userEscrow = UserEscrowDetails()
        userEscrow.setFromNewEscrowReq(newUserEscrowRequest)
        userEscrow.setFromNewEscrowResp(responseObj)

        return userEscrow        


    def closeUserEscrow(self, escrow: UserEscrowDetails) -> bool:
        return self.closeUserEscrowById(escrow.escrowId)


    def closeUserEscrowById(self, userEscrowId: str) -> bool:

        endpoint = '/userescrow/close'

        request = apiRequests.APICloseUserEscrowRequest(userEscrowId)
        response = self.sendRequest(endpoint, request.to_dict())

        responseOjb = apiResponses.api_close_escrow_response_from_dict(response)

        return responseOjb.close


    # Exchange Escrow Management
    def createNewExchEscrow(
        self,
        exchId: str,
        reserveAddress: str,
        exchEscrowCurrency: sf.Blockchain,
        amount: float,
        userEscrowId: str,
        expiryTime: int) -> ExchEscrowDetails:

        endpoint = '/exchescrow/create'

        request = apiRequests.APINewExchangeEscrowRequest(exchId, exchEscrowCurrency, amount, expiryTime, reserveAddress, userEscrowId)
        response = self.sendRequest(endpoint, request.to_dict())
        
        responseObj = apiResponses.api_new_exchange_escrow_response_from_dict(response)

        exchEscrow = ExchEscrowDetails()
        exchEscrow.setFromNewEscrowReq(requests)
        exchEscrow.setFromNewEscrowResp(responseObj)

        return exchEscrow


    def priceExchEscrow(
        self,
        exchId: str,
        exchEscrowCurrency: sf.Blockchain,
        amount: float,
        expiryTime: int,
        userCurrencies: list()):
        
        endpoint = '/exchescrow/price'

        request = apiRequests.APIPriceExchangeEscrowRequest(exchId, exchEscrowCurrency, amount, expiryTime, userCurrencies)
        response = self.sendRequest(endpoint, request.to_dict())
        
        responseObj = apiResponses.api_escrow_fee_response_from_dict(response)

        return responseObj


    def closeExchEscrow(self, exchEscrow: ExchEscrowDetails) -> bool:
        return self.closeExchEscrowById(exchEscrow.escrowId)


    def closeExchEscrowById(self, exchEscrowId: str) -> bool:

        endpoint = '/userescrow/close'

        request = apiRequests.APICloseExchangeEscrowRequest(exchEscrowId)
        response = self.sendRequest(endpoint, request.to_dict())

        responseOjb = apiResponses.api_close_escrow_response_from_dict(response)

        return responseOjb.close


    def feeHistory(self, startTime: int) -> apiResponses.APIEscrowFeeHistoryResponse:

        endpoint = '/exchescrow/feehistory'

        request = apiRequests.APIHistoryRequest(startTime)
        response = self.sendRequest(endpoint, request.to_dict())

        responseObj = apiResponses.api_escrow_fee_history_from_dict(response)

        return responseObj


    def queryOrdersById(self, orderId: str) -> OrderDetails:
        return (self.queryOrders(orderId))[0]


    def queryOrders(
        self,
        orderId = None, 
        fromTime = None, 
        isOpen = True, 
        limit = 1000, 
        exchId = None) -> list():

        endpoint = '/orders/query'

        request = apiRequests.APIFilterRequest(orderId, fromTime, limit, exchId, not isOpen)
        response = self.sendRequest(endpoint, request.to_dict())

        responseObj = apiResponses.api_order_query_response_from_dict(response)
        
        return responseObj


    def newSellOrder(self, 
        userEscrow: UserEscrowDetails, 
        exchEscrow: ExchEscrowDetails,
        amount: float) -> OrderDetails:

        endpoint = '/orders/quote'

        symbol = sf.Symbol(exchEscrow.currency, userEscrow.currency)

        request = apiRequests.APIPlaceOrderRequest(sf.OrderType.RFQ.value, symbol.toString(), sf.TimeInForce.FOK.value, None, amount, sf.Side.SELL.value, userEscrow.escrowId, exchEscrow.escrowId)

        response = self.sendRequest(endpoint, requests)
        responseObj = apiResponses.api_place_order_response_from_dict(response)

        order = OrderDetails()

        order.updateOrderFromRequest(request)
        order.updateOrderFromRequest(responseObj)

        return order


    def newBuyOrder(self, 
        userEscrow: UserEscrowDetails, 
        exchEscrow: ExchEscrowDetails,
        amount: float) -> OrderDetails:

        endpoint = '/orders/quote'

        symbol = sf.Symbol(exchEscrow.currency, userEscrow.currency)

        request = apiRequests.APIPlaceOrderRequest(sf.OrderType.RFQ.value, symbol.toString(), sf.TimeInForce.FOK.value, None, amount, sf.Side.BUY.value, userEscrow.escrowId, exchEscrow.escrowId)

        response = self.sendRequest(endpoint, request.to_dict())
        responseObj = apiResponses.api_place_order_response_from_dict(response)

        order = OrderDetails()

        order.updateOrderFromRequest(request)
        order.updateOrderFromRequest(responseObj)

        return order


    def executeById(self, orderId: str) -> bool:
        
        endpoint = '/orders/execute'

        request = apiRequests.APIOrderIDRequest(orderId)
        response = self.sendRequest(endpoint, request.to_dict())

        responseObj = apiResponses.api_order_executed_response_from_dict(response)

        return responseObj.executed


    def execute(self, order: OrderDetails) -> bool:
        return self.executeById(order.orderId)


    def cancelById(self, orderId: str) -> bool:

        endpoint = '/orders/cancel'
        
        request = apiRequests.APIOrderIDRequest(orderId)
        response = self.sendRequest(endpoint, request.to_dict())

        responseObj = apiResponses.api_order_canceled_response_from_dict(response)

        return responseObj.canceled


    def cancel(self, order: OrderDetails) -> bool:
        return self.cancelById(order.orderId)


    def inquirePrice(self, 
        userEscrowId: str, 
        exchEscrowId: str, 
        amount: float, 
        side: sf.Side) -> apiResponses.APIOrderInquiryResponse:

        endpoint = '/orders/inquiry'

        request = apiRequests.APIOrderInquiryRequest(userEscrowId, exchEscrowId, amount, side.value)
        response = self.sendRequest(endpoint, request.to_dict())

        responseObj = apiResponses.api_order_inquiry_response_from_dict(response)

        return responseObj
