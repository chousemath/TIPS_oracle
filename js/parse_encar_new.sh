#!/bin/bash

set -o nounset                              # Treat unset variables as an error

while true
do
    # python parse_encar_new.py
    aws s3 cp encar_new.csv s3://trive-forecast-01/encar_new.csv
    echo 'sleeping for 5h'
    sleep 5h
done
