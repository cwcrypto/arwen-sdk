__all__ = ['ArwenConfig']

import json

class ArwenConfig:
    def __init__(self):
        self.ip = None
        self.port = None
        self.testnetBTC = None
        self.testnetBCH = None
        self.testnetLTC = None
        self.testnetETH = None
        self.testnetApiKey = None
        self.testnetApiSecret = None
        self.mainnetBTC = None
        self.mainnetBCH = None
        self.mainnetLTC = None
        self.mainnetETH = None

    def loadConfig(self, filePath):
        with open(filePath, 'r') as configText:
            configJson = json.loads(configText.read())

            self.ip = configJson['ip']
            self.port = configJson['port']
            self.testnetBTC = configJson['testnetBTC']
            self.testnetLTC = configJson['testnetLTC']
            self.testnetBCH = configJson['testnetBCH']
            self.testnetETH = configJson['testnetETH']
            self.testnetApiKey = configJson['testnetApiKey']
            self.testnetApiSecret = configJson['testnetApiSecret']
            self.mainnetBTC = configJson['mainnetBTC']
            self.mainnetBCH = configJson['mainnetBCH']
            self.mainnetLTC = configJson['mainnetLTC']
            self.mainnetETH = configJson['mainnetETH']

    
