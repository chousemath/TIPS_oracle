#!/bin/bash

while true
do
    node carmanager.js
    cd pages_list_carmanager
    grep -r 'javascript:carmangerDetailWindowPopUp' . | sort --unique > ../carmanager_links.txt
    cd ..
    python carmanager_scripts.py
    node carmanager_detail.js
    node cm_selection.js
done
