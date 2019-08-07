#!/bin/bash

# start 5 instances of the encar (domestic only) scraper
for run in {1..5}
do
  forever start encardata.js
done

# start 5 instances of the encar (foreign only) scraper
for run in {1..5}
do
  forever start encardata.js -c foreign
done

