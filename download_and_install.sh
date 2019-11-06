TAG=0.19.0
TAG_STRING="${TAG//\./-}"

wget https://cwc-trading-app-releases.s3.amazonaws.com/arwen-sdk-beta-testnet-$TAG_STRING.tar

docker load < arwen-sdk-beta-testnet-$TAG_STRING.tar

wget https://cwc-trading-app-releases.s3.amazonaws.com/arwen-sdk-beta-mainnet-$TAG_STRING.tar

docker load < arwen-sdk-beta-mainnet-$TAG_STRING.tar

docker volume create arwen-database

rm arwen-sdk*.tar

docker image ls