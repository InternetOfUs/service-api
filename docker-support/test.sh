#!/bin/bash

docker run -it --rm ${IMAGE_NAME} ./run_tests.sh
        if [ $? != 0 ]; then
            echo "ERR: One or more tests are failing"
            clean
            exit 1
        fi