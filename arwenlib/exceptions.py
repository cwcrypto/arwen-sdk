class SystemException(Exception):
    error: str
    stackTrace: str

    def __init__(self, error: str, data: str):
        self.error = error
        self.stackTrace = data

class ProtocolException(Exception):
    error: str
    stackTrace: str
    
    def __init__(self, error: str, data: str):
        self.error = error
        self.stackTrace = data