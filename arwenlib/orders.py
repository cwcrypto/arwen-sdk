__all__ = ['OrderDetails']

from . import supportFunctions as sf
from .messages import apiResponses, apiRequests
import json
from time import time

class OrderDetails:
    orderId: str
    userEscrowId: str
    exchEscrowId: str
    orderType: sf.OrderType
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
        self.orderType = sf.OrderType.RFQ
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
        self.side = sf.Side(request.side)
        self.symbol = sf.Symbol.fromString(request.symbol)
        self.timeCreated = int(time())

        return self

    def updateOrderFromResponse(self, response: apiResponses.APIPlaceOrderResponse):
        self.orderId = response.order_id
        self.userEscrowAmount = response.sell_amount
        self.exchEscrowAmount = response.buy_amount
        self.price = response.price
        self.timeExpiry = response.quote_expiry

        return self

    def setFromQuery(self, response: apiResponses.APIOrderResponseElement):
        self.orderId = response.order_id
        self.orderType = sf.OrderType(response.orderType)
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

        return self

    def __repr__(self):
        return f'''OrderDetails
                orderId:        {self.orderId}
                orderType:      {self.orderType.value}
                orderState:     {self.state.value}
                symbol:         {self.symbol}
                side:           {self.side}
                exchEscrowId:   {self.exchEscrowId}
                userEscrowId:   {self.userEscrowId}
                exchAmount:     {self.exchEscrowAmount}
                userAmount:     {self.userEscrowAmount}
                price:          {self.price} {self.symbol.quote.value}/{self.symbol.base.value} (LOCAL ESTIMATE)
                timeCreated:    {self.timeCreated}
                timeClosed:     {self.timeClosed}'''