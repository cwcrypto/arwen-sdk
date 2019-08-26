import requests
import json
import math
import pprint

import supportFunctions as sf
import accountManagement as acc
import baseEscrowDetails as baseDetails
import userEscrow
import exchEscrow
import orders

import constants as c

if __name__ == "__main__":
    resp = acc.initArwenClient()
    print(resp.text)
    time = acc.timeArwenClient()
    print(time.text)
    register = acc.registerApiKeys()
    # print(register)

    userEscrowId = 501
    exchEscrowId = 417

    ue = userEscrow.userEscrowDetails().setFromEscrowId(userEscrowId)
    ee = exchEscrow.exchEscrowDetails().setFromEscrowId(exchEscrowId)

    print('tradeBot will wait until escrow has been funded and confirmed by user')
    sf.waitForEscowToOpen(ue)

    print('tradeBot will wait until escrow has been funded and confirmed by exchange')
    sf.waitForEscowToOpen(ee)

    ### TRADING BELOW ###

    print('Creating a sell order of 0.01 BTC for LTC')

    order = orders.sellTrade(ue, ee, 0.01)
    print('Order Details:')
    pprint.pprint(order)

    input(f'press key to send execute order 30 second timeout')

    execute = orders.execute(order)
    print(f'Order Execution: {execute}')

    ee.updateEscrowDetails()
    print('Updated user Escrow details, notice the trade(s) made')
    pprint.pprint(ee.trades)

    # Returns a stack error if you have no malformed escrows
    # resp = acc.cleanupBadEscrows()
    # pprint.pprint(resp)
