import os
import sys

sys.path.append("../")
import arwenlib.ArwenClient as arwen
import arwenlib.supportFunctions as sf
from arwenlib import constants as c

from arwenlib import startArwenClient

client = startArwenClient()

url = client.getOAuthUrl(exchId=sf.Exchange.KUCOIN)

print('Below is your kyc URL. Please copy-paste this into a web browser to finish the process')
print(url)

input('Please press any button to continue and check your KYC status')

status = client.getKycStatus(exchId=sf.Exchange.KUCOIN)

print(status)