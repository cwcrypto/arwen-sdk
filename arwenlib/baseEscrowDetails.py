__all__ = ['EscrowDetails', 'FiltersRequest']

from . import supportFunctions as sf

from . import constants as c

from .messages import apiResponses, apiRequests

import json

class EscrowDetails:
    exchId: str
    escrowId: str
    escrowAddress: str
    escrowType: sf.EscrowType
    state: sf.EscrowState
    currency: sf.Blockchain
    amount: float
    expiryTime: int
    availableToTrade: float
    trades: list()
    amountSentToUserReserve: float
    timeCreated: int
    timeClosed: int

    def __init__(self):
        self.exchId = None
        self.escrowId = None
        self.escrowAddress = None
        self.state = sf.EscrowState.UNKNOWN
        self.currency = None
        self.amount = 0
        self.expiryTime = 0
        self.availableToTrade = -1
        self.trades = list()
        self.amountSentToUserReserve = -1
        self.timeCreated = -1
        self.timeClosed = -1
        self.escrowType = None

    def setFromNewEscrowReq(self, request):
        if isinstance(request, apiRequests.APINewUserEscrowRequest):
            self.currency = sf.Blockchain(request.user_escrow_currency)
            self.amount = request.amount
            self.availableToTrade = self.amount

        if isinstance(request, apiRequests.APINewExchangeEscrowRequest):
            self.currency = sf.Blockchain(request.exch_escrow_currency)
            self.amount = request.amount
            self.availableToTrade = self.amount

    def setFromQuery(self, queryResponse):
        raise NotImplementedError("This is an abstract class, please use User/ExchEscrowDetails classes")

    def toString(self):
        return str(self.__dict__)

class FiltersRequest:
    def __init__(self):
        self.params = dict().fromkeys(['fromTime', 'isFinal', 'limit', 'exchId'])
    
    def setFilter(self, escrowType, escrowId, startTime, isOpen, limit, exchId):

        if(escrowId != None):
            self.params[f'{escrowType.value}EscrowId'] = escrowId
        else:
            self.params['fromTime'] = startTime
            self.params['isFinal'] = not isOpen
            self.params['limit'] = limit
            self.params['exchId'] = exchId

    def getFilter(self):
        return self.params
