#!/bin/bash

grep -r 'javascript:carmangerDetailWindowPopUp' . | awk '{print substr($0, 54, 40)}' | awk 'index($0, "carmangerDetailWindowPopUp")' | awk '{print substr($0, 29, 100)}' | grep -o '[0-9]\+' | sort --unique > ../carmanager_links.txt
