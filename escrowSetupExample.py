import requests
import json
import math
import pprint

from arwenlib import ArwenClient as Arwen
from arwenlib import baseEscrowDetails as baseDetails
from arwenlib import supportFunctions as sf

from arwenlib import startArwenClient

import constants as c

if __name__ == "__main__":
    client = startArwenClient()

    exchInfo = client.exchanges()
    pprint.pprint(exchInfo)

    register = client.registerApiKeys(c.testnetApiKey, c.testnetApiSecret)
    pprint.pprint(register)


    newUE = client.createNewUserEscrow(c.testnetBTC)
    print('User Escrow (Unfunded)')
    print(f'userEscrowId:    {newUE.escrowId}')
    print(f'address to fund: {newUE.escrowAddress}')
    print(f'amount to fund:  {newUE.amountToFund}')

    print('tradeBot will wait until escrow has been funded and confirmed by user')
    sf.waitForEscowToOpen(newUE, client)

    print('All user escrows that are not closed:')
    queryUE = client.queryEscrows(sf.EscrowType.USER)
    pprint.pprint(queryUE)

    newEE = client.createNewExchEscrow(c.testnetLTC, userEscrow=newUE)
    print('Exchage Escrow (Funded by Exchage Automatically)')
    print(f'exchEscrowId:    {newEE.escrowId}')
    print(f'escrow address:  {newEE.escrowAddress}')
    print(f'pricePaid:       {newEE.pricePaid}')

    print('tradeBot will wait until escrow has been funded and confirmed by exchange')
    sf.waitForEscowToOpen(newEE, client)

    print('All exch escrows that are not closed:')
    queryEE = client.queryEscrows(sf.EscrowType.EXCH)
    pprint.pprint(queryEE)

    print('Hooray! You have set up a user and exchange escrow!')
    print('Write down your user and exchange escrowId and try the simpleBot script!')