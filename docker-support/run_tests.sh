#!/bin/bash

#cd scrip ts

python -m unittest discover tests/wenet_service_api_test
if [ $? != 0 ]; then
    echo "ERR: Tests for model module failed"
    exit 1
fi
