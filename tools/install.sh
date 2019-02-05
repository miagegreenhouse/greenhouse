#!/bin/bash 

if [ -z "$1" ]
then
    echo "No argument supplied
    Usage : ./install.sh <env>
    env can be : local, dev, prod"
else
    if [ $1 == "local" ] || [ $1 == "dev" ] || [ $1 == "prod" ]
    then
      DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
      print $DIR
      $DIR/../greenhouse-server/install.sh $1
    else
        echo "Bad argument supplied
        Usage : ./install.sh <env>
        env can be : local, dev, prod"
    fi
fi
