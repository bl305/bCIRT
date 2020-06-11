#!/usr/bin/env bash
#pip freeze --local | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U
#pip freeze | cut -d = -f 1 | xargs -n 1 pip search | grep -B2 'LATEST:'
#in venv
pip3 list -o --format columns|  cut -d' ' -f1 #|xargs -n1 pip install -U
