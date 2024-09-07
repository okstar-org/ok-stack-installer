#!/bin/bash

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
    DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
    SOURCE="$(readlink "$SOURCE")"
    [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

VERSION_REG="{ok-stack-{ce|ee}:beta|ok-stack-{ce|ee}:latest|ok-stack-{ce|ee}:v{version}}"

if [ -z "$1" ]; then
    echo "Using ./install.sh $VERSION_REG"
    exit 1
fi

version=$1

if [[ $version =~ ^(ok-stack-(ce|ee):(beta|latest|v[0-9]+\.[0-9]+\.[0-9]+))$ ]]; then
    echo "Matched version: $version"
else
    echo "Version does not match the pattern $VERSION_REG."
    exit 1
fi

echo "version is: $version"

echo "VERSION=$version" > depends/.env

python3 init.py
echo "Install is completed."