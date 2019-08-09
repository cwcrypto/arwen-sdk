import requests 
import json
import enum
import time

import constants as c

class Side(enum.Enum): 
    BUY = 'BUY'
    SELL = 'SELL'

class Exchange(enum.Enum): 
    BINONCE = 'Binonce'

class Blockchain(enum.Enum): 
    BTC = 'BTC'
    LTC = 'LTC'
    BCH = 'BCH'
    ETH = 'ETH'

    @staticmethod
    def FromString(currency):
        for b in Blockchain:
            if(b.value.lower == currency.lower):
                return b


class State(enum.Enum):
    OPEN = 'OPEN'
    OPENING = 'OPENING'
    CLOSED = 'CLOSED'
    UNKNOWN = 'UNKNOWN'

    @staticmethod
    def FromString(state):
        for s in State:
            if(s.value.lower == state.lower):
                return s

class OrderType(enum.Enum): 
    rfq = 'RFQ'

class timeInForce(enum.Enum):
    fok = 'FOK'


class Symbol(): 
    def __init__(self, quoteCurrency, baseCurrency):
        self.quote = quoteCurrency # should be Blockchain
        self.base = baseCurrency # should be Blockchain
        self.separator = '-'

    def toString(self):
        return f'{self.quote.value}{self.separator}{self.base.value}'

def generateEscrowTimelock(days):
    if(days < 1.0):
        raise AttributeError('timelock can not be less than 1 day', days)

    return int(time.time() + (24 * 60 * 60 * days) + 10)


def sendRequest(url, endpoint, params = None):

    if(params == None):
        params = dict()

    return  json.loads(requests.post(f'{url}{endpoint}', json=params).text)
