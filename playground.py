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
    
    testUserEscrow = userEscrow.userEscrowLite(501, sf.Blockchain.BTC)
    query = baseDetails.queryEscrows(testUserEscrow.escrowType, testUserEscrow.escrowId)[0]
    newUE = userEscrow.userEscrowDetails()
    newUE.setFromQuery(query)