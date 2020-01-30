#!/bin/bash

echo "Extracting all car ids and car types"
grep -r 'window.open("/dc/dc_carsearchpop.do?method=getInstallment&carid=' . | awk '{print substr($2,59, 24)}' > ../car_ids.txt
echo "Finished extraction"
