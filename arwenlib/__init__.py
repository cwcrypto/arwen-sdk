__author__ = 'Nabeel Younis for Arwen Secure'
__name__ = 'arwenlib'

__all__ = [
    'startArwenClient',
    'ArwenClient',
    'baseEscrowDetails',
    'constants',
    'escrowRequests',
    'exchEscrow',
    'orders',
    'supportFunctions',
    'transactions',
    'userEscrow'
    ]


def startArwenClient(ip='127.0.0.1', port='5000'):
    import arwenlib.ArwenClient as Arwen

    client = Arwen.ArwenClient(ip, port)

    client.initArwenService()

    return client



