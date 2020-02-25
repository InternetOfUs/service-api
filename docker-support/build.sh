#!/bin/bash

DEFAULT_VERSION="0.0.2"

clean () {
    rm -R -f ${SCRIPT_DIR}/src
    rm -R ${SCRIPT_DIR}/requirements.txt
    rm -R ${SCRIPT_DIR}/tests
    rm -R ${SCRIPT_DIR}/docs
}

SCRIPT_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
PROJECT_DIR=${SCRIPT_DIR}/..

# Identifying build version

VERSION=$1
if [ -z "${VERSION}" ]; then
    VERSION=${DEFAULT_VERSION}
    echo "Build version not specified: building with default version [${VERSION}]"
else
    echo "Building with specified version [${VERSION}]"
fi

mkdir ${SCRIPT_DIR}/src
mkdir ${SCRIPT_DIR}/tests
mkdir ${SCRIPT_DIR}/docs
cp -R ${PROJECT_DIR}/src/* ${SCRIPT_DIR}/src
cp ${PROJECT_DIR}/requirements.txt ${SCRIPT_DIR}
cp -R ${PROJECT_DIR}/tests/* ${SCRIPT_DIR}/tests
cp -R ${PROJECT_DIR}/docs/* ${SCRIPT_DIR}/docs


# Building image

IMAGE_NAME=wenet/wenet_service_api:${VERSION}
docker build -t ${IMAGE_NAME} ${SCRIPT_DIR}
if [ $? == 0 ]; then

    echo "Build successful: ${IMAGE_NAME}"

    # Running tests

    if [[ "${SKIP_TESTS}" -eq "1" ]]; then
        echo "WARN: Forcing test skipping"
    else
        docker run -it --rm ${IMAGE_NAME} ./run_tests.sh
        if [ $? != 0 ]; then
            echo "ERR: One or more tests are failing"
            clean
            exit 1
        fi
    fi

    # Tagging images for registry

    echo "Tagging image for push to registry.u-hopper.com:5000"
    docker tag ${IMAGE_NAME} registry.u-hopper.com:5000/${IMAGE_NAME}
    echo "Image can be pushed with:"
    echo "- docker push registry.u-hopper.com:5000/${IMAGE_NAME}"
    # Cleaning
    clean

    exit 0

else
    echo "ERR: Build failed for ${IMAGE_NAME}"
    # Cleaning
    clean

    exit 1
fi

