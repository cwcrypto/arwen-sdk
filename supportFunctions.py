import requests 
import json
import enum
import time

import constants as c
import baseEscrowDetails as baseDetails


class EscrowType(enum.Enum): 
    USER = 'user'
    EXCH = 'exch'

class Side(enum.Enum): 
    BUY = 'BUY'
    SELL = 'SELL'

class Exchange(enum.Enum): 
    BINONCE = 'Binonce'

class OrderType(enum.Enum): 
    RFQ = 'RFQ'

class timeInForce(enum.Enum):
    FOK = 'FOK'

class Blockchain(enum.Enum): 
    BTC = 'BTC'
    LTC = 'LTC'
    BCH = 'BCH'
    ETH = 'ETH'

class EscrowState(enum.Enum):
    OPENING = 'OPENING'
    OPEN = 'OPEN'
    TRADING = 'TRADING'
    CLOSED = 'CLOSED'
    UNKNOWN = 'UNKNOWN'

class OrderState(enum.Enum):
    OPEN = 'OPEN'
    EXECUTED = 'EXECUTED'
    CANCELD = 'CANCELED'
    EXPIRED = 'EXPIRED'
    UNKNOWN = 'UNKNOWN'

class Symbol(): 
    def __init__(self, quoteCurrency, baseCurrency):
        self.quote = quoteCurrency # should be Blockchain
        self.base = baseCurrency # should be Blockchain
        self.separator = '-'

    def fromString(self, sym):
        b,q = sym.split('-')
        self.quote = q
        self.base = b
        return self

    def toString(self):
        return f'{self.quote.value}{self.separator}{self.base.value}'


def generateEscrowTimelock(days):
    if(days < 1.0):
        raise AttributeError('Timelock can not be less than 1 day', days)

    return int(time.time() + (24 * 60 * 60 * days) + 10)


def waitForEscowToOpen(escrow):

    if(escrow.state == EscrowState.CLOSED or escrow.state == EscrowState.UNKNOWN):
        return False

    while(escrow.state != EscrowState.OPEN):
        escrow.updateEscrowDetails()
        print('Waiting 60 seconds before next poll...')
        time.sleep(60)

    return True


def sendRequest(url, endpoint, params = None):

    if(params == None):
        params = dict()

    resp = requests.post(f'{url}{endpoint}', json=params).text

    if(resp == None or resp == ''):
        return None

    return  json.loads(resp)
