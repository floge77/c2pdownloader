#! /bin/bash

DOWNLOADDIR=$HOME/downloads
if [[ ! -d "$DOWNLOADDIR" ]]; then
    echo "please create a directory named downloads at $HOME"
    exit 1
fi
CONFIG=$(pwd)/config.yaml
if [[ ! -f "$CONFIG" ]]; then
    echo "Please create a config.yaml where you executed that script."
    exit 1
fi

echo HELLO 
docker stop cloud2podcast
docker rm cloud2podcast
docker run -d --name c2pdownloader --rm -v $(pwd)/config.yaml:/config.yaml -v $HOME/downloads:/downloads c2pdownloader
docker run --rm --name cloud2podcast -p 80:8080 -v $HOME/downloads:/downloads -e HOST_IP="cloud2podcast" -e port=80 -it floge77/cloud2podcastpi
