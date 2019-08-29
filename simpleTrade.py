import requests
import json
import math
import pprint

from arwenlib import ArwenClient as Arwen
from arwenlib import supportFunctions as sf

from arwenlib import startArwenClient

import constants

if __name__ == "__main__":
    c = constants.ArwenConfig()
    c.loadConfig()

    client = startArwenClient(c.ip, c.port)

    client.registerApiKeys(c.testnetApiKey, c.testnetApiSecret)

    time = client.timeArwenClient()
    print(f'ArwenClient time:{time}')

    ping = client.pingArwenClient()
    print(f'ArwenClient ping: {ping}')

    userEscrowIdBtc = 509
    exchEscrowIdLtc = 417
    exchEscrowIdBch = 418

    ueBtc = client.getEscrowById(sf.EscrowType.USER, userEscrowIdBtc)
    eeLtc = client.getEscrowById(sf.EscrowType.EXCH, exchEscrowIdLtc)

    print('tradeBot will wait until escrow has been funded and confirmed by user')
    sf.waitForEscowToOpen(ueBtc, client)

    print('tradeBot will wait until escrow has been funded and confirmed by exchange')
    sf.waitForEscowToOpen(eeLtc, client)

    ### TRADING BELOW ###

    print('Creating a sell order of 0.01 BTC for LTC')

    order = client.sellTrade(ueBtc, eeLtc, 0.01)
    print('Order Details:')
    pprint.pprint(order)

    input(f'press key to send execute order 30 second timeout')

    execute = client.execute(order)
    print(f'Order Execution: {execute}')

    ueBtc = client.updateEscrowDetails(ueBtc)
    print('Updated user Escrow details, notice the trade(s) made')
    pprint.pprint(ueBtc.trades)

    # Returns a stack error if you have no malformed escrows
    # resp = acc.cleanupBadEscrows()
    # pprint.pprint(resp)
