__all__ = ['EscrowDetails', 'FiltersRequest']

import arwenlib.supportFunctions as sf

import constants as c

class EscrowDetails:
    def __init__(self):
        self.escrowId = None
        self.escrowAddress = None
        self.state = None
        self.currency = None
        self.amount = None
        self.expiryTime = None
        self.availableToTrade = None
        self.trades = list()
        self.amountSentToUserReserve = None
        self.timeCreated = None
        self.timeClosed = None
        self.escrowType = None

    def setFromQuery(self, queryResponse):        
        self.escrowId = queryResponse[f'{self.escrowType.value}EscrowId']
        self.escrowAddress = queryResponse['escrowAddress']
        self.state = sf.EscrowState(queryResponse['state'])
        self.currency = sf.Blockchain(queryResponse[f'{self.escrowType.value}EscrowCurrency'])
        self.amount = float(queryResponse['amount'])
        self.availableToTrade = float(queryResponse['availableToTrade'])
        self.trades = queryResponse['trades']
        self.amountSentToUserReserve = float(queryResponse['amountSentToUserReserve'])
        self.timeCreated = int(queryResponse['timeCreated'])
        self.timeClosed = int(queryResponse['timeClosed'])
        
        return self

    def setFromNewEscrowReq(self, req):
        self.currency = sf.Blockchain(req[f'{self.escrowType.value}EscrowCurrency'])
        self.availableToTrade = float(req['qty'])
        self.amount = float(req['qty'])

        return self

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
