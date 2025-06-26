#!/bin/bash
set -e

cd pokerstove-master
mkdir -p build
cd build
cmake ..
make -j4
cp bin/ps-eval ../..

