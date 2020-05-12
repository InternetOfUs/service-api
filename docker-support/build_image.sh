#!/bin/bash

DEFAULT_VERSION="0.0.3"

clean () {
    rm -R -f ${SCRIPT_DIR}/src
    rm -R ${SCRIPT_DIR}/requirements.txt
    rm -R ${SCRIPT_DIR}/tests
    rm -R ${SCRIPT_DIR}/docs
}

SCRIPT_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
PROJECT_DIR=${SCRIPT_DIR}/..

# Identifying build version

mkdir ${SCRIPT_DIR}/src
mkdir ${SCRIPT_DIR}/tests
mkdir ${SCRIPT_DIR}/docs
cp -R ${PROJECT_DIR}/src/* ${SCRIPT_DIR}/src
cp ${PROJECT_DIR}/requirements.txt ${SCRIPT_DIR}
cp -R ${PROJECT_DIR}/tests/* ${SCRIPT_DIR}/tests
cp -R ${PROJECT_DIR}/docs/* ${SCRIPT_DIR}/docs
cp -R ${PROJECT_DIR}/wenet-common-models/src/* ${SCRIPT_DIR}/src
cp -R ${PROJECT_DIR}/wenet-common-models/test/* ${SCRIPT_DIR}/tests


# Building image

docker build --cache-from ${REGISTRY}/${IMAGE_NAME} -t ${IMAGE_NAME} ${SCRIPT_DIR}
if [ $? == 0 ]; then

    echo "Build successful: ${IMAGE_NAME}"

    # Tagging images for registry

    echo "Tagging image for push to registry.u-hopper.com"
    docker tag ${IMAGE_NAME} ${REGISTRY}/${IMAGE_NAME}
    echo "Image can be pushed with:"
    echo "- docker push registry.u-hopper.com/${IMAGE_NAME}"
    # Cleaning
    clean

    exit 0

else
    echo "ERR: Build failed for ${IMAGE_NAME}"
    # Cleaning
    clean

    exit 1
fi

