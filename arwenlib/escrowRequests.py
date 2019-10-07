__all__ = ['NewExchEscrowRequest', 'NewUserEscrowRequest']

from . import supportFunctions as sf

class NewExchEscrowRequest:
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
        import arwenlib.exchEscrow as exchEscrow
        ee = exchEscrow.ExchEscrowDetails()
        ee.setFromNewEscrowReq(self.params)
        ee.setFromNewEscrowResp(self.resp)
        return ee

class NewUserEscrowRequest:
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
        import arwenlib.userEscrow as userEscrow

        ue = userEscrow.UserEscrowDetails()
        ue.setFromNewEscrowReq(self.params)
        ue.setFromNewEscrowResp(self.resp)
        return ue