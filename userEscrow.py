import constants as c
import supportFunctions as sf
import baseEscrowDetails as baseDetails


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

class userEscrowDetails(baseDetails.escrowDetails):
    def __init__(self):
        self.escrowType = sf.EscrowType.USER
        self.state = sf.EscrowState.OPENING

    def setFromNewEscrowResp(self, resp):
        self.escrowId = resp['userEscrowId']
        self.escrowAddress = resp['escrowAddress']
        self.amountToFund = float(resp['amountToFund'])

        return self


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