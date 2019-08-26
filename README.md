# tradeBot
Python3 trading bot example for interacting with arwen-api

Download and install arwen-api: `download_and_install.sh`

Start the docker image: `start_api.sh`

Run the tradeBot:

```
python simpleBot.py
```

Close Arwen Client

```
docker kill arwen
```

API Documentation
https://arwenclient.docs.apiary.io/

Prerequisites:
 - [wget](https://www.gnu.org/software/wget/manual/wget.html)
 - python 3.6+
 - Docker

Notes:
 - For python, please create a virtual environment with the [requirements](./reqs.txt) installed
 - The funding flow requires the trader to fund escrows using a hot wallet outside of arwen-api before continuing with making trades
 - Allow time for user and exchange escrows to confirmed to be open before trying to make trades (can take up to 30 minutes for escrows to confirm on testnet)
 - Set your reserve [addresses](./constants.py)

For support please open an issue.