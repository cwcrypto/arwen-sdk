import supportFunctions as sf
import constants as c
import baseEscrowDetails as baseDetails


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
        self.params['userEscrowId'] = userEscrow.escrowId
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


class exchEscrowDetails(baseDetails.escrowDetails):
    def __init__(self):
        self.pricePaid = None
        self.escrowType = sf.EscrowType.EXCH
        self.state = sf.EscrowState.OPENING

    def setFromNewEscrowResp(self, resp):
        self.escrowId = resp['exchEscrowId']
        self.escrowAddress = resp['escrowAddress']
        self.pricePaid = float(resp['pricePaid'])
        self.expiryTime = int(resp['expiryTime'])
        self.state = sf.EscrowState.OPENING

        return self


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


def closeExchEscrow(exchEscrowId):

    endpoint = '/exchescrow/close'

    params = dict()
    params['exchEscrowId'] = exchEscrowId

    resp = sf.sendRequest(c.url, endpoint, params)

    return resp['closed']