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
        pass

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

    def __repr__(self):
        return f'''{self.escrowType} Escrow
                exchId:         {self.exchId}
                {self.escrowType.value}EscrowId:   {self.escrowId}
                escrowAddress:  {self.escrowAddress}
                escrowState:    {self.state}
                escrowCurrency: {self.currency}
                totalAmount:    {self.amount}
                tradableAmount: {self.availableToTrade}
                trades:         {self.trades}
                sentToYou:      {self.amountSentToUserReserve}
                timeCreated:    {self.timeCreated}
                timeClosed:     {self.timeClosed}'''

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

    
