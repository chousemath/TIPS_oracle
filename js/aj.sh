#!/bin/bash -
#===============================================================================
#
#          FILE: gen_links_encar.sh
#
#         USAGE: ./gen_links_encar.sh
#
#   DESCRIPTION:
#
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: YOUR NAME (),
#  ORGANIZATION:
#       CREATED: 01/21/2020 09:23:58
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error

while true
do
    node aj.js 
    python parse_pages_list_aj.py 
    node aj_detail.js
done


