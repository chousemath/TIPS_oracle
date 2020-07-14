#!/bin/bash

set -o nounset                              # Treat unset variables as an error

while true
do
    python parse_carmanager.py
    python aws_forecast_01.py
done
