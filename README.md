**DOWNLOAD LINKS DOWN UNTIL MONDAY MORNING**

# arwenlib
Python3.6.8 interface example for interacting with Arwen Client. Arwen Client is a dockerized version of the Arwen application that enables users to create escrows and perform atomic swaps programmatically. 

API Documentation and explanation of Arwen:
https://arwenclient.docs.apiary.io/

## What is arwenlib:
Arwenlib is an example how to build a trading system on top of the Arwen Client. In this repo we have built a library capable of interacting with ArwenClient, it will parse messages and maintain data structures in memory. You can write a trading bot on top of arwenlib if you would like, or implement your own in any language, although arwenlib is by no means meant for production systems. 

## How to use arwenlib
Our [sample scripts](./sampleScripts) demonstrate how to build a cli using arwenlib. Each script will instantiate a messenger, the messenger will sign in to ArwenClient and then be ready to generate requests and parse responses. The sample scripts are provided as an example of how to use arwenlib, they are not intended to be used for any production systems.

## Writing your own trading system
The docker container can be thought of as an exchange hosting an API you want to trade against. You can build a trading system in any language you want.

Prerequisites:
 - [wget](https://www.gnu.org/software/wget/manual/wget.html)
 - [python 3.6.8](https://www.python.org/downloads/release/python-368/)
 - [Docker](https://hub.docker.com/)


Download and install arwen-api (depending on your machine you may need sudo): 
```
./download_and_install.sh
```

Start the docker image:
```
./start_api_NETWORK.sh  # mainnet or testnet
```

By default the start script will run a testnet mode of Arwen in the background. If you would like to see the log output remove the `-d` flag from this script. To switch to mainnet mode, change run this script with the mainnet version of the docker.

General trading flow:
 - Open and fund user escrow and wait for confirmation
 - Request exchange escrow and pay the fee with existing user escrow 
 - Trade between user and exchange escrows (unidirectional only, from user to exchange)
 - Close escrows for a fee rebate

Escrow Setup Example:

[Open a user escrow](./sampleScripts/openUserEscrow.py)
```
 $ python3.6 openUserEscrow.py -b LTC -e Binonce -q 1.0 -t 1.0 -r YOUR_LTC_ADDRESS
 > Signed In
 > escrowId:           585
 > fundingAddress:     QPGnZTxt32Cs3qFZUNyiotpANaqhrWqiAY
 > amountToFund:       1.0001692
 > Waiting 60 seconds before next poll...
 > Waiting 60 seconds before next poll...
 > Escrow opened successfully
```

[Open an exchange escrow](./sampleScripts/openExchangeEscrow.py)
```
 $ python3.6 openExchangeEscrow.py -b BTC -e Binonce -q 0.005 -t 2.0 -u 585 -r YOUR_BTC_ADDRESS
 > Signed In
 > escrowId:         477
 > escrow address:   2N8v6scLUrG27CWDkfyUBqSE74pNZF7kbCZ
 > escrow fee:       0.0000141496 LTC
 > Waiting 60 seconds before next poll...
 > Waiting 60 seconds before next poll...
 > Waiting 60 seconds before next poll...
 > Waiting 60 seconds before next poll...
 > Waiting 60 seconds before next poll...
 > Escrow opened successfully
```

[Request a trade](./sampleScripts/makeTrade.py)
```
 $ python3.6 makeTrade.py -u 585 -e 477 -q 0.1 -s SELL
 > OrderId: 543
```

[Request a trade](./sampleScripts/executeTrade.py)
```
 $ python3.6 executeTrade.py -i 543
 > executed: True
```


Close Arwen Client:
```
docker kill arwen
```

Notes:
 - For python, please create a virtual environment of python3.6.8 with the [requirements](./reqs.txt) installed
 - The funding flow requires the trader to fund escrows using a hot wallet outside of arwen-api before continuing with making trades
 - Allow time for user and exchange escrows to confirmed to be open before trying to make trades (can take up to 30 minutes for escrows to confirm on testnet)
 - Set your reserve [addresses](./constants.py)

For support please open an issue.