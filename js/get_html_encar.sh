#!/bin/bash -
#===============================================================================
#
#          FILE: get_html_encar.sh
#
#         USAGE: ./get_html_encar.sh
#
#   DESCRIPTION:
#
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: YOUR NAME (),
#  ORGANIZATION:
#       CREATED: 01/21/2020 09:26:30
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error

while true
do
    node encar_detail.js
done

