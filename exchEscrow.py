import supportFunctions as sf
import constants as c

class filters:
    def __init__(self):
        self.params = dict().fromkeys(['fromTime', 'isFinal', 'limit', 'exchId'])
    
    def setFilter(self, exchEscrowId, startTime, isOpen, count, exchId):

        if(exchEscrowId != None):
            self.params['exchEscrowId'] = exchEscrowId
        else:
            self.params['fromTime'] = startTime
            self.params['isFinal'] = not isOpen
            self.params['limit'] = count
            self.params['exchId'] = exchId

    def getFilter(self):
        return self.params


class newExchEscrowRequest:
    def __init__(self):
        self.params = dict().fromkeys(['exchId','exchEscrowCurrency','expiryTime',
            'qty', 'reserveAddress', 'maxPrice', 'userEscrowId',
            'userEscrowCurrency'])

        self.resp = dict().fromkeys(['escrowAddress', 'pricePaid', 'exchEscrowId'])

    def setup(self, exchId, exchEscrowCurrency, expiryTime, qty, reserveAddress,
        maxPrice, userEscrow):
        
        if not isinstance(exchId, sf.Exchange):
            raise TypeError('Invalid Exchange passed')
        
        if not isinstance(userEscrow.currency, sf.Blockchain):
            raise TypeError('Invalid Blockchain passed')

        if not isinstance(exchEscrowCurrency, sf.Blockchain):
            raise TypeError('Invalid Blockchain passed')

        self.params['exchId'] = exchId.value
        self.params['exchEscrowCurrency'] = exchEscrowCurrency.value
        self.params['expiryTime'] = expiryTime
        self.params['qty'] = str(qty)
        self.params['reserveAddress'] = reserveAddress
        self.params['maxPrice'] = str(maxPrice)
        self.params['userEscrowId'] = userEscrow.userEscrowId
        self.params['userEscrowCurrency'] = userEscrow.currency.value

    def getRequest(self):
        return self.params
    
    def setResponse(self, newEscrowResponse):
        self.resp = newEscrowResponse

    def createUserEscrowDetails(self):
        ee = exchEscrowDetails()
        ee.setFromNewEscrowReq(self.params)
        ee.setFromNewEscrowResp(self.resp)
        return ee


class exchEscrowDetails:
    def __init__(self):
        self.exchEscrowId = None
        self.escrowAddress = None
        self.state = None
        self.currency = None
        self.amount = None
        self.expiryTime = None
        self.availableToTrade = None
        self.trades = list()
        self.amountSentToUserReserve = None
        self.pricePaid = None
        self.timeCreated = None
        self.timeClosed = None

    def setFromQuery(self, queryResponse):
        self.exchEscrowId = queryResponse['exchEscrowId']
        self.escrowAddress = queryResponse['escrowAddress']
        self.state = sf.State.FromString(queryResponse['state'])
        self.currency = sf.Blockchain.FromString(queryResponse['exchEscrowCurrency'])
        self.amount = float(queryResponse['amount'])
        self.availableToTrade = float(queryResponse['availableToTrade'])
        self.trades = queryResponse['trades']
        self.amountSentToUserReserve = float(queryResponse['amountSentToUserReserve'])
        self.timeCreated = int(queryResponse['timeCreated'])
        self.timeClosed = int(queryResponse['timeClosed'])

    def setFromNewEscrowReq(self, req):
        self.currency = sf.Blockchain.FromString(req['exchEscrowCurrency'])
        self.availableToTrade = float(req['qty'])
        self.amount = float(req['qty'])

    def setFromNewEscrowResp(self, resp):
        self.exchEscrowId = resp['exchEscrowId']
        self.escrowAddress = resp['escrowAddress']
        self.pricePaid = float(resp['pricePaid'])
        self.expiryTime = int(resp['expiryTime'])
        self.state = sf.State.OPEN

class exchEscrowLite():
    def __init__(self, eeid, currency):
        self.exchEscrowId = eeid
        self.currency = currency
        self.params = dict()
        self.params['exchEscrowId'] = eeid
        self.params['currency'] = currency

    def getRequest(self):
        return self.params

def historyUserEscrows(startTime = None):

    endpoint = '/exchescrow/history'

    queryParams = dict()
    queryParams['startTime'] = startTime

    exchEscrowIdList = sf.sendRequest(c.url, endpoint, queryParams)

    return exchEscrowIdList


def queryExchEscrows(exchEscrowId = None, startTime = None, isOpen = True, limit = 1000, exchId = None):

    endpoint = '/exchescrow/query'

    queryParams = filters()
    queryParams.setFilter(exchEscrowId, startTime, isOpen, limit, exchId)

    exchEscrowList = sf.sendRequest(c.url, endpoint, queryParams.getFilter())

    return exchEscrowList


def priceExchEscrow(
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

    return sf.sendRequest(c.url, endpoint, params)

def createNewExchEscrow(
    exchId=sf.Exchange.BINONCE,
    exchEscrowCurrency=sf.Blockchain.LTC,
    qty=2.0,
    expiryTime=sf.generateEscrowTimelock(2.0),
    maxPrice=0.005,
    userEscrow=None,
    reserveAddress=c.testnetLTC):
    
    endpoint = '/exchescrow/create'

    newEEReq = newExchEscrowRequest()
    newEEReq.setup(exchId, exchEscrowCurrency, expiryTime, qty, reserveAddress,
        maxPrice, userEscrow)
    
    resp = sf.sendRequest(c.url, endpoint, newEEReq.getRequest())
    newEEReq.setResponse(resp)

    return newEEReq.createUserEscrowDetails()

def closeExchEscrow(exchEscrowId):

    endpoint = '/exchescrow/close'

    params = dict()
    params['exchEscrowId'] = exchEscrowId

    resp = sf.sendRequest(c.url, endpoint, params)

    return resp['closed']