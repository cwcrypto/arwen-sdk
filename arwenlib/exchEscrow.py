__all__ = ['ExchEscrowDetails']

from . import supportFunctions as sf
from . import baseEscrowDetails as baseDetails


class ExchEscrowDetails(baseDetails.EscrowDetails):
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