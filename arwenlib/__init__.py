__author__ = 'Nabeel Younis for Arwen Secure'
__name__ = 'arwenlib'

__all__ = [
    'startArwenClient',
    'ArwenClient',
    'baseEscrowDetails',
    'constants',
    'exceptions',
    'exchEscrow',
    'orders',
    'supportFunctions',
    'userEscrow'
    ]


def startArwenClient(ip='127.0.0.1', port='5000'):
    from . import ArwenClient as Arwen

    client = Arwen.ArwenClient(ip, port)

    resp = client.initArwenService()
    print(resp.text)

    return client



