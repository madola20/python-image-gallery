#!/usr/bin/bash

if [ "$#" != "1" ]; then
    echo "Usage: activate <version-number>"
    exit 1

fi

rm -f ec2-scripts/ec2-prod-latest.sh

cd ec2-scripts
ln -s ec2-scripts/ec2-prod-$1.sh ec2-prod-latest.sh
cd ..

./deploy $1
./deploy latest
