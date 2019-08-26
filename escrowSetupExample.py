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

    exchInfo = acc.exchanges()
    pprint.pprint(exchInfo)

    register = acc.registerApiKeys()
    pprint.pprint(register)

    newUE = userEscrow.createNewUserEscrow()
    print('User Escrow (Unfunded)')
    print(f'userEscrowId:    {newUE.escrowId}')
    print(f'address to fund: {newUE.escrowAddress}')
    print(f'amount to fund:  {newUE.amountToFund}')

    print('tradeBot will wait until escrow has been funded and confirmed by user')
    sf.waitForEscowToOpen(newUE)

    print('All user escrows that are not closed:')
    queryUE = baseDetails.queryEscrows(sf.EscrowType.USER)
    pprint.pprint(queryUE)

    newEE = exchEscrow.createNewExchEscrow(userEscrow=newUE)
    print('Exchage Escrow (Funded by Exchage Automatically)')
    print(f'exchEscrowId:    {newEE.escrowId}')
    print(f'escrow address:  {newEE.escrowAddress}')
    print(f'pricePaid:       {newEE.pricePaid}')

    print('tradeBot will wait until escrow has been funded and confirmed by exchange')
    sf.waitForEscowToOpen(newEE)

    print('All exch escrows that are not closed:')
    queryEE = baseDetails.queryEscrows(sf.EscrowType.EXCH)
    pprint.pprint(queryEE)

    print('Escrow')