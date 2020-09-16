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
    aws s3 cp carmanager_allowed.json s3://trive-forecast-01/carmanager_allowed.json
    aws s3 cp carmanager_colors.json s3://trive-forecast-01/carmanager_colors.json
    aws s3 cp carmanager_transmissions.json s3://trive-forecast-01/carmanager_transmissions.json
    aws s3 cp carmanager_accidents.json s3://trive-forecast-01/carmanager_accidents.json
    aws s3 cp carmanager_warranties.json s3://trive-forecast-01/carmanager_warranties.json
    aws s3 cp carmanager_years.json s3://trive-forecast-01/carmanager_years.json
done
