TAG=0.20.7

docker run --rm --name arwen -p 5000:5000 -v arwen-database:/arwenDatabase arwen-sdk/beta-testnet:$TAG