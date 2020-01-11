#! /bin/bash

DOWNLOADDIR=$HOME/downloads
if [! -d "$DOWNLOADDIR" ]; then
    echo "please create a directory named downloads at $HOME"
    exit 1
fi
CONFIG=$(pwd)/config.yaml
if [! -d "$CONFIG" ]; then
    echo "Please create a config.yaml where you executed that script."
    exit 1
fi


docker run -d --name c2pdownloader --rm -v $(pwd)/config.yaml:/config.yaml -v $HOME/downloads:/downloads c2pdownloader
