TAG=0.18.2

docker run --rm --name arwen -p 5000:5000 -v arwen-database:/arwenDatabase arwen-sdk/beta-mainnet:$TAG