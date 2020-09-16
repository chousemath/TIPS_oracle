#!/bin/bash

set -o nounset                              # Treat unset variables as an error

while true
do
    python parse_carmanager.py
    python aws_forecast_01.py
    python aws_forecast_02.py
    python carmanager_transmissions.py
    aws s3 cp carmanager_forecast.csv s3://trive-forecast-01/carmanager_forecast.csv
    aws s3 cp carmanager_forecast.json s3://trive-forecast-01/carmanager_forecast.json
    aws s3 cp carmanager_sales.csv s3://trive-forecast-01/carmanager_sales.csv
done
