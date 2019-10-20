__all__ = ['UserEscrowDetails',]

from . import supportFunctions as sf
from . import baseEscrowDetails as baseDetails
from .messages import apiResponses


class UserEscrowDetails(baseDetails.EscrowDetails):
    amountToFund: float
    
    def __init__(self):
        self.escrowType = sf.EscrowType.USER
        self.state = sf.EscrowState.UNKNOWN

    def setFromQuery(self, queryResponse: apiResponses.APIUserEscrowElement):
        self.exchId = queryResponse.exch_id
        self.escrowId = queryResponse.user_escrow_id
        self.escrowAddress = queryResponse.escrow_address
        self.state = sf.EscrowState(queryResponse.state)
        self.currency = sf.Blockchain(queryResponse.user_escrow_currency)
        self.amount = queryResponse.amount
        self.availableToTrade = queryResponse.available_to_trade
        self.trades = queryResponse.trades
        self.amountSentToUserReserve = queryResponse.amount_sent_to_reserve
        self.timeCreated = queryResponse.time_created
        self.timeClosed = queryResponse.time_closed

    def setFromNewEscrowResp(self, response: apiResponses.APINewUserEscrowResponse):
        self.escrowId = response.user_escrow_id
        self.escrowAddress = response.escrow_address
        self.amountToFund = response.amount_to_fund
        self.state = sf.EscrowState.OPENING

        return self