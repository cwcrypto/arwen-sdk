import requests
import json
import math
import pprint

from arwenlib import ArwenClient as Arwen
from arwenlib import supportFunctions as sf

from arwenlib import startArwenClient

import constants as c

if __name__ == "__main__":
    client = startArwenClient()

    client.registerApiKeys(c.testnetApiKey, c.testnetApiSecret)

    time = client.timeArwenClient()
    print(f'ArwenClient time:{time.text}')

    ping = client.pingArwenClient()
    print(f'ArwenClient ping: {ping.text}')

    userEscrowId = 501
    exchEscrowId = 417

    ue = client.getEscrowById(sf.EscrowType.USER, userEscrowId)
    ee = client.getEscrowById(sf.EscrowType.EXCH, exchEscrowId)

    print('tradeBot will wait until escrow has been funded and confirmed by user')
    sf.waitForEscowToOpen(ue, client)

    print('tradeBot will wait until escrow has been funded and confirmed by exchange')
    sf.waitForEscowToOpen(ee, client)

    ### TRADING BELOW ###

    print('Creating a sell order of 0.01 BTC for LTC')

    order = client.sellTrade(ue, ee, 0.0001)
    print('Order Details:')
    pprint.pprint(order)

    input(f'press key to send execute order 30 second timeout')

    execute = client.execute(order)
    print(f'Order Execution: {execute}')

    ue = client.updateEscrowDetails(ue)
    print('Updated user Escrow details, notice the trade(s) made')
    pprint.pprint(ue.trades)

    # Returns a stack error if you have no malformed escrows
    # resp = acc.cleanupBadEscrows()
    # pprint.pprint(resp)
