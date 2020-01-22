#!/bin/bash -
#===============================================================================
#
#          FILE: setup.sh
#
#         USAGE: ./setup.sh
#
#   DESCRIPTION:
#
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: YOUR NAME (),
#  ORGANIZATION:
#       CREATED: 01/22/2020 19:15:49
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error

# builds all cython modules
python setup.py build_ext --inplace

