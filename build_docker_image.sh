#!/bin/bash

DEFAULT_VERSION="latest"

VERSION=$2
if [ -z "${VERSION}" ]; then
    VERSION=${DEFAULT_VERSION}
    echo "Version not specified: building with default version [${VERSION}]"
else
    echo "Using specified version [${VERSION}]"
fi

SCRIPT_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

$SCRIPT_DIR/docker-support/runner.sh -bti $VERSION