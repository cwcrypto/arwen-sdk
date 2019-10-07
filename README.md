# tradeBot
Python3 trading example for interacting with arwen-api

Prerequisites:
 - [wget](https://www.gnu.org/software/wget/manual/wget.html)
 - [python 3.6.8](https://www.python.org/downloads/release/python-368/)
 - [Docker](https://hub.docker.com/)


Download and install arwen-api: 

```
./download_and_install.sh
```

Start the docker image: 

```
start_api.sh
```


General trading flow:
 - Open and fund user and exchange escrows for the currencies you want to trade in, keeping in mind that you can only trade from a user escrow to an exchange escrow
 - Trade between user and exchange escrows
 - Close escrows for a fee rebate

Escrow Setup Example:

```
python escrowSetupExample.py
```

Take the user and exchange escrow ids from the previous script and edit them into simpleTrade.py then run it

```
python simpleBot.py
```


Close Arwen Client

```
docker kill arwen
```

API Documentation
https://arwenclient.docs.apiary.io/


Notes:
 - For python, please create a virtual environment of python3.6.8 with the [requirements](./reqs.txt) installed
 - The funding flow requires the trader to fund escrows using a hot wallet outside of arwen-api before continuing with making trades
 - Allow time for user and exchange escrows to confirmed to be open before trying to make trades (can take up to 30 minutes for escrows to confirm on testnet)
 - Set your reserve [addresses](./constants.py)

For support please open an issue.