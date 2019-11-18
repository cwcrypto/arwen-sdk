__all__ = ['EscrowType', 'Side', 'Exchange', 'OrderType', 'TimeInForce', 'Blockchain', 'EscrowState', 'OrderState', 'Symbol', 'generateEscrowTimelock', 'waitForEscowToOpen']

import requests 
import json
import enum
import time

from . import ArwenClient as Arwen 


class EscrowType(enum.Enum): 
    USER = 'user'
    EXCH = 'exch'

class Side(enum.Enum): 
    BUY = 'BUY'
    SELL = 'SELL'

class Exchange(enum.Enum): 
    # Testnet
    BINONCE = 'Binonce' 
    TRACKEN = 'Tracken'
    COINBOSS = 'Coinboss'
    ROLONIEX = 'Roloniex'
    BITFINESSE = 'Bitfinesse'
    # Mainnet
    KUCOIN = 'kucoinrfq'

class OrderType(enum.Enum): 
    RFQ = 'RFQ'

class TimeInForce(enum.Enum):
    FOK = 'FOK'

class Blockchain(enum.Enum): 
    BTC = 'BTC'
    LTC = 'LTC'
    BCH = 'BCH'
    ETH = 'ETH'
    UNKNOWN = 'UNKNOWN'

class EscrowState(enum.Enum):
    # User has requested a new Exchange/User Escrow
    # but it has not yet been accepted by the exchange
    PENDING = 'PENDING'

    # First state for an Exchange Escrow after being created
    # Remains in this state until user has paid the fee for the escrow
    UNPAID_FEE = 'UNPAID_FEE'

    # Temporary trading state for a User Escrow while making
    # a sendFee request (signing cashout) for an Exchange Escrow
    PAYING_FEE = 'PAYING_FEE'
    
    # Exchange rejected request for escrow
    # or the Escrow was canceled by the user/exchange
    # or the Escrow expired without funding
    REJECTED = 'REJECTED'
    
    # Waiting for the Escrow to be funded on the blockchain
    # and to receive safe block count number of confirmations
    UNCONFIRMED = 'UNCONFIRMED'
    
    # Escrow funding transaction is confirmed on the blockchain
    # Trading is now allowed with this escrow
    OPEN = 'OPEN'
    
    # This escrow is currently being used as part of an uncompleted RFQ trade
    TRADING = 'TRADING'
    
    # A cooperative cashout tx has been signed by the hub and client
    # or an escrow closing tx has been detected on the blockchain
    # Waiting for safe block count confirmation of the closing tx
    CLOSING = 'CLOSING'
    
    # Marks this escrow as expiring soon- cannot be used for trading.
    # Should only be allowed to close an Escrow in EXPIRING
    EXPIRING = 'EXPIRING'
    
    # The escrow has been closed (spent) by a transaction that
    # already has safe block count confirmations
    CLOSED = 'CLOSED'
    
    # The escrow is placed into frozen state after it was part of a
    # aborted RFQ trade. A User or Exchange Escrow in FROZEN cannot be
    # used for trading and can only be cooperatively or unilaterally
    # closed. The escrow only move out of FROZEN state when CLOSED
    FROZEN = 'FROZEN'
    
    # Fallback state, if you see this please tell me
    UNKNOWN = 'UNKNOWN'

class OrderState(enum.Enum):
    OPEN = 'OPEN'
    EXECUTED = 'EXECUTED'
    CANCELLED = 'CANCELLED'
    EXPIRED = 'EXPIRED'
    UNKNOWN = 'UNKNOWN'

class Symbol(): 
    def __init__(self, quoteCurrency: Blockchain, baseCurrency: Blockchain):
        self.quote = quoteCurrency
        self.base = baseCurrency
        self.separator = '-'

    @staticmethod
    def fromString(sym):
        quote, base = sym.split('-')
        return Symbol(Blockchain(quote), Blockchain(base))

    def __repr__(self):
        return f'{self.quote.value}{self.separator}{self.base.value}'

    def toString(self):
        return self.__repr__()


def generateEscrowTimelock(days: float):
    if(days < 1.0):
        raise AttributeError('Timelock can not be less than 1 day', days)

    return int(time.time() + (24 * 60 * 60 * days) + 10)


def waitForEscowToOpen(escrow, client):

    if not isinstance(client, Arwen.ArwenClient):
        raise AttributeError('client passed is not an ArwenClient')

    if(escrow.state == EscrowState.CLOSED or escrow.state == EscrowState.UNKNOWN):
        return False

    while(escrow.state != EscrowState.OPEN):
        escrow = client.queryEscrowById(escrow.escrowType, escrow.escrowId)
        print('Waiting 60 seconds before next poll...')
        time.sleep(60)

    return True
