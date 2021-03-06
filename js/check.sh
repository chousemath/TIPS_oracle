#!/bin/bash

autopep8 --in-place --recursive *.py
mypy cparse_pages_list.pyx 
mypy cparse_pages_list_aj.pyx
mypy cparse_pages_list_encar_domestic.pyx
mypy cparse_pages_list_mpark.pyx
mypy cdecompose.pyx

mypy decompose.py \
    parse_pages_list.py \
    parse_pages_list_aj.py \
    parse_pages_list_encar_domestic.py \
    parse_pages_list_mpark.py \
    process_aj_01.py \
    encar_exporter.py \
    mpark_exporter.py \
    mpark_parser.py \
    aj_exporter.py \
    setup.py
