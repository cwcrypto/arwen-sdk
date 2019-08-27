__all__ = ['UserEscrowDetails',]

import arwenlib.supportFunctions as sf
import arwenlib.baseEscrowDetails as baseDetails


class UserEscrowDetails(baseDetails.EscrowDetails):
    def __init__(self):
        self.escrowType = sf.EscrowType.USER
        self.state = sf.EscrowState.OPENING

    def setFromNewEscrowResp(self, resp):
        self.escrowId = resp['userEscrowId']
        self.escrowAddress = resp['escrowAddress']
        self.amountToFund = float(resp['amountToFund'])

        return self