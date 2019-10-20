__all__ = ['OrderDetails']

from . import supportFunctions as sf
from .messages import apiResponses, apiRequests
import json
from time import time

class OrderDetails:
    orderId: str
    userEscrowId: str
    exchEscrowId: str
    ordertype: sf.OrderType
    side: sf.Side
    symbol: sf.Symbol
    exchEscrowAmount: float
    userEscrowAmount: float
    timeInForce: sf.TimeInForce
    price: float
    timeCreated: int
    timeExpiry: int
    timeClosed: int

    def __init__(self):
        self.orderId = None
        self.userEscrowId = None
        self.exchEscrowId = None
        self.ordertype = sf.OrderType.RFQ
        self.side = None
        self.symbol = None
        self.exchEscrowAmount = None
        self.userEscrowAmount = None
        self.timeInForce = sf.TimeInForce.FOK
        self.price = None           # Not used at the moment
        self.timeCreated = None
        self.timeExpiry = None
        self.timeClosed = None

    def updateOrderFromRequest(self, request: apiRequests.APIPlaceOrderRequest):
        self.userEscrowId = request.user_escrow_id
        self.exchEscrowId = request.exch_escrow_id
        self.side = request.side
        self.symbol = request.symbol
        self.timeCreated = int(time())

    def updateOrderFromResponse(self, response: apiResponses.APIPlaceOrderResponse):
        self.orderId = response.order_id
        self.userEscrowAmount = response.sell_amount
        self.exchEscrowAmount = response.buy_amount
        self.price = response.price
        self.timeExpiry = response.quote_expiry

    def setFromQuery(self, response: apiResponses.APIOrderResponseElement):
        self.ordertype = sf.OrderType(response.orderType)
        self.state = sf.OrderState(response.state)
        self.symbol = sf.Symbol.fromString(response.symbol)
        self.exchEscrowAmount = response.exch_escrow_amount
        self.userEscrowAmount = response.user_escrow_amount
        self.price = float(self.exchEscrowAmount / self.userEscrowAmount)
        self.exchEscrowId = response.exch_escrow_id
        self.userEscrowId = response.user_escrow_id
        self.side = sf.Side(response.side)
        self.timeCreated = response.time_created
        self.timeClosed = response.time_closed

    def toString(self):
        return self.__dict__