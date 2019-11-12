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
    OPENING = 'OPENING'
    OPEN = 'OPEN'
    TRADING = 'TRADING'
    CLOSED = 'CLOSED'
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
        return Symbol(quote, base)

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
