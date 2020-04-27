#!/bin/bash

python -m unittest discover tests
if [ $? != 0 ]; then
    echo "ERR: Tests failed"
    exit 1
fi

