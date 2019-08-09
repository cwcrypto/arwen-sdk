import constants as c
import supportFunctions as sf

class filters:
    def __init__(self):
        self.params = dict().fromkeys(['userEscrowId', 'fromTime', 'isFinal', 'limit', 'exchId'])
    
    def setFilter(self, userEscrowId, startTime, isOpen, count, exchId):

        if(userEscrowId != None):
            self.params['userEscrowId'] = userEscrowId
        else:
            self.params['fromTime'] = startTime
            self.params['isFinal'] = not isOpen
            self.params['limit'] = count
            self.params['exchId'] = exchId

    def getFilter(self):
        return self.params

class newUserEscrowRequest:
    def __init__(self):
        self.params = dict().fromkeys(['exchId','userEscrowCurrency','expiryTime',
            'qty', 'reserveAddress'])

        self.resp = dict().fromkeys(['escrowAddress', 'amountToFund', 'userEscrowId'])

    def setup(self, exchId, currency, expiryTime, qty, reserveAddress):
        
        if not isinstance(exchId, sf.Exchange):
            raise TypeError('Invalid Exchange passed')

        if not isinstance(currency, sf.Blockchain):
            raise TypeError('Invalid Blockchain passed')

        self.params['exchId'] = exchId.value
        self.params['userEscrowCurrency'] = currency.value
        self.params['expiryTime'] = expiryTime
        self.params['qty'] = str(qty)
        self.params['reserveAddress'] = reserveAddress

    def getRequest(self):
        return self.params
    
    def setResponse(self, newEscrowResponse):
        self.resp = newEscrowResponse

    def createUserEscrowDetails(self):
        ue = userEscrowDetails()
        ue.setFromNewEscrowReq(self.params)
        ue.setFromNewEscrowResp(self.resp)
        return ue

class userEscrowDetails:
    def __init__(self):
        self.userEscrowId = None
        self.escrowAddress = None
        self.state = None
        self.currency = None
        self.amount = None
        self.availableToTrade = None
        self.trades = list()
        self.amountSentToUserReserve = None
        self.timeCreated =None
        self.timeClosed = None
        
    def setFromQuery(self, queryResponse):
        self.userEscrowId = queryResponse['userEscrowId']
        self.escrowAddress = queryResponse['escrowAddress']
        self.state = sf.State.FromString(queryResponse['state'])
        self.currency = sf.Blockchain.FromString(queryResponse['userEscrowCurrency'])
        self.amount = float(queryResponse['amount'])
        self.availableToTrade = float(queryResponse['availableToTrade'])
        self.trades = queryResponse['trades']
        self.amountSentToUserReserve = float(queryResponse['amountSentToUserReserve'])
        self.timeCreated = int(queryResponse['timeCreated'])
        self.timeClosed = int(queryResponse['timeClosed'])
    
    def setFromNewEscrowReq(self, req):
        self.currency = sf.Blockchain.FromString(req['userEscrowCurrency'])
        self.availableToTrade = float(req['qty'])
        self.amount = float(req['qty'])

    def setFromNewEscrowResp(self, resp):
        self.userEscrowId = resp['userEscrowId']
        self.escrowAddress = resp['escrowAddress']
        self.amountToFund = float(resp['amountToFund'])

class userEscrowLite():
    def __init__(self, ueid, currency):
        self.userEscrowId = ueid
        self.currency = currency
        self.params = dict()
        self.params['userEscrowId'] = ueid
        self.params['currency'] = currency

    def getRequest(self):
        return self.params


def historyUserEscrows(startTime = None):

    endpoint = '/userescrow/history'

    queryParams = dict()
    queryParams['startTime'] = startTime

    userEscrowIdList = sf.sendRequest(c.url, endpoint, queryParams)

    return userEscrowIdList

def queryUserEscrows(userEscrowId = None, startTime = None, isOpen = True, limit = 1000, exchId = None):

    endpoint = '/userescrow/query'

    queryParams = filters()
    queryParams.setFilter(userEscrowId, startTime, isOpen, limit, exchId)

    userEscrowList = sf.sendRequest(c.url, endpoint, queryParams.getFilter())

    return userEscrowList


def createNewUserEscrow(exchId = sf.Exchange.BINONCE,
    currency = sf.Blockchain.BTC, 
    expiryTime = sf.generateEscrowTimelock(2.0), 
    qty = 0.025, 
    reserveAddress = c.testnetBTC):

    endpoint = '/userescrow/create'

    newUEReq = newUserEscrowRequest()
    newUEReq.setup(exchId, currency, expiryTime, qty, reserveAddress)

    resp = sf.sendRequest(c.url, endpoint, newUEReq.getRequest())
    newUEReq.setResponse(resp)

    return newUEReq.createUserEscrowDetails()


def closeUserEscrow(userEscrowId):

    endpoint = '/userescrow/close'

    params = dict()
    params['userEscrowId'] = userEscrowId

    resp = sf.sendRequest(c.url, endpoint, params)

    return resp['closed']
