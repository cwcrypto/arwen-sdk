__all__ = ['ArwenConfig']

import json

class ArwenConfig:
    def __init__(self):
        self.ip = None
        self.port = None
        self.testnetBTC = None
        self.testnetBCH = None
        self.testnetLTC = None
        self.testnetApiKey = None
        self.testnetApiSecret = None
        self.mainnetBTC = None
        self.mainnetBCH = None
        self.mainnetLTC = None

    def loadConfig(self, filePath = 'config.json'):
        with open(filePath, 'r') as configText:
            configJson = json.loads(configText.read())

            self.ip = configJson['ip']
            self.port = configJson['port']
            self.testnetBTC = configJson['testnetBTC']
            self.testnetLTC = configJson['testnetLTC']
            self.testnetBCH = configJson['testnetBCH']
            self.testnetApiKey = configJson['testnetApiKey']
            self.testnetApiSecret = configJson['testnetApiSecret']
            self.mainnetBTC = configJson['mainnetBTC']
            self.mainnetBCH = configJson['mainnetBCH']
            self.mainnetLTC = configJson['mainnetLTC']

    
