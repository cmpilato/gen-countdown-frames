#!/bin/bash

if [ "$1" == "--check-only" ]; then
    BLACK_ARGS=" --check"
else
    BLACK_ARGS=""
fi

black --line-length=100 $BLACK_ARGS src || exit 1
flake8 --config=flake8.conf src || exit 1