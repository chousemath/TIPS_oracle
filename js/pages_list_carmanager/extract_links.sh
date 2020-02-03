#!/bin/bash

grep -r 'javascript:carmangerDetailWindowPopUp' . | sort --unique > ../carmanager_links.txt
