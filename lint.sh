#!/bin/bash

black --line-length=100 --check gen-countdown-frames || exit 1
flake8 --config=flake8.conf gen-countdown-frames || exit 1