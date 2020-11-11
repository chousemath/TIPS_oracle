#!/bin/bash

set -o nounset                              # Treat unset variables as an error

while true
do
    # python parse_encar_new.py
    aws s3 cp encar_new2.csv s3://trive-forecast-01/encar_new2.csv
    echo 'sleeping for 10h'
    sleep 10h
done
