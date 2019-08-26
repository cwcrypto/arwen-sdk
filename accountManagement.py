import requests
import constants as c
import supportFunctions as sf


def initArwenClient():
    return requests.post(f'{c.url}/init')

def pingArwenClient():
    return requests.get(f'{c.url}/ping')

def timeArwenClient():
    return requests.get(f'{c.url}/time')

def cleanupBadEscrows():
    
    endpoint = '/cleanup'
    
    return sf.sendRequest(c.url, endpoint)

def exchanges():

    endpoint = '/exchanges'

    return sf.sendRequest(c.url, endpoint)

def registerApiKeys():

    endpoint = '/register'

    reqParams = dict()
    reqParams['exchId'] = 'Binonce'
    reqParams['apiKey'] = c.testnetApiKey
    reqParams['apiSecret'] = c.testnetApiSecret

    return sf.sendRequest(c.url, endpoint, reqParams)


def feeHistory(startTime = None):

    endpoint = '/feehistory'

    reqParams = dict()
    reqParams['startTime'] = startTime

    return sf.sendRequest(c.url, endpoint, reqParams)