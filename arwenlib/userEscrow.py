__all__ = ['UserEscrowDetails',]

from . import supportFunctions as sf
from . import baseEscrowDetails as baseDetails
from .messages import apiResponses


class UserEscrowDetails(baseDetails.EscrowDetails):
    amountToFund: float
    fundingAddress: str
    
    def __init__(self):
        self.escrowType = sf.EscrowType.USER
        self.state = sf.EscrowState.UNKNOWN

    def setFromQuery(self, queryResponse: apiResponses.APIUserEscrowElement):
        self.exchId = sf.Exchange(queryResponse.exch_id)
        self.escrowId = queryResponse.user_escrow_id
        self.escrowAddress = queryResponse.escrow_address
        self.state = sf.EscrowState(queryResponse.state)
        self.currency = sf.Blockchain(queryResponse.user_escrow_currency)
        self.amount = queryResponse.amount
        self.availableToTrade = queryResponse.available_to_trade
        self.trades = queryResponse.trades
        self.amountSentToUserReserve = queryResponse.amount_sent_to_user_reserve
        self.timeCreated = queryResponse.time_created
        self.timeClosed = queryResponse.time_closed
        self.amountToFund = queryResponse.amount_to_fund
        self.fundingAddress = queryResponse.funding_address

        return self

    def setFromNewEscrowResp(self, response: apiResponses.APINewUserEscrowResponse):
        self.escrowId = response.user_escrow_id
        self.escrowAddress = response.escrow_address
        self.amountToFund = response.amount_to_fund
        self.state = sf.EscrowState.OPENING

        return self

    def __repr__(self):
        return f'''{super().__repr__()}
                fundingAddress: {self.fundingAddress}
                fundingAmount:  {self.amountToFund}'''