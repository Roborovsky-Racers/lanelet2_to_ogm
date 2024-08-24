#!/bin/bash

SCRIPT_DIR=`dirname $0`
cd ${SCRIPT_DIR}

if [ ! -d ".venv" ]; then
  python3 -m venv .venv
  source .venv/bin/activate
  python3 -m virtualenv -p python3.8 .virtualenv
  source .virtualenv/bin/activate
  pip install -r requirements.txt
else
  source .virtualenv/bin/activate
fi

python3 lanelet2_to_ogm.py