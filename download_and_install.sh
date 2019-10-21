wget https://cwc-trading-app-releases.s3.amazonaws.com/arwen-sdk-external-testnet-0-1.tar

docker load < arwen-api-external-testnet.tar

wget https://cwc-trading-app-releases.s3.amazonaws.com/arwen-sdk-external-mainnet-0-1.tar

docker load < arwen-api-external-mainnet.tar

docker volume create arwen-database

rm arwen-api*.tar

docker image ls