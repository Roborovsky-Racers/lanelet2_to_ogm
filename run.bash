#!/bin/bash

SCRIPT_DIR=`dirname $0`
cd ${SCRIPT_DIR}

if [ ! -d ".venv" ]; then
  python3 -m venv .venv
  source .venv/bin/activate
  pip install pyyaml
  pip install lanelet2
  pip install numpy
  pip install opencv-python
else
  source .venv/bin/activate
fi

python3 lanelet2_to_ogm.py