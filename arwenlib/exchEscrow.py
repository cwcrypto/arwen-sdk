__all__ = ['ExchEscrowDetails']

from . import supportFunctions as sf
from . import baseEscrowDetails as baseDetails
from .messages import apiResponses


class ExchEscrowDetails(baseDetails.EscrowDetails):
    escrowFeePaid = float

    def __init__(self):
        self.escrowFeePaid = None
        self.escrowType = sf.EscrowType.EXCH
        self.state = sf.EscrowState.UNKNOWN

    def setFromQuery(self, queryResponse: apiResponses.APIExchangeEscrowElement):
        self.exchId = sf.Exchange(queryResponse.exch_id)
        self.escrowId = queryResponse.exch_escrow_id
        self.escrowAddress = queryResponse.escrow_address
        self.state = sf.EscrowState(queryResponse.state)
        self.currency = sf.Blockchain(queryResponse.exch_escrow_currency)
        self.amount = queryResponse.amount
        self.availableToTrade = queryResponse.available_to_trade
        self.trades = queryResponse.trades
        self.amountSentToUserReserve = queryResponse.amount_sent_to_reserve
        self.timeCreated = queryResponse.time_created
        self.timeClosed = queryResponse.time_closed

        return self

    def setFromNewEscrowResp(self, resp: apiResponses.APINewExchangeEscrowResponse):
        self.escrowId = resp.exch_escrow_id
        self.escrowAddress = resp.escrow_address
        self.escrowFeePaid = resp.escrow_fee_paid
        self.state = sf.EscrowState.OPENING

        return self

    def __repr__(self):
        return f'''{super().__repr__()}
                escrowFeePaid: {self.escrowFeePaid}'''