#!/bin/bash 

if [ -z "$1" ]
then
    echo "No argument supplied
    Usage : ./install.sh <env>
    env can be : local, dev, prod"
else
    if [ $1 == "local" ] || [ $1 == "dev" ] || [ $1 == "prod" ]
    then
      ../greenhouse-server/install.sh
    else
        echo "Bad argument supplied
        Usage : ./install.sh <env>
        env can be : local, dev, prod"
    fi
fi
