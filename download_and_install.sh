wget https://cwc-trading-app-releases.s3.amazonaws.com/arwen-api.tar

docker load < arwen-api.tar

docker volume create arwen-database

rm arwen-api.tar

docker image ls
