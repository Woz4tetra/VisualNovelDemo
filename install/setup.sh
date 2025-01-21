#!/bin/bash
BASE_DIR=$(realpath "$(dirname $0)")

sudo apt-get update
sudo apt-get install -y libopenblas-dev
${BASE_DIR}/install_python_deps.sh
