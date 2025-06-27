#!/bin/bash
set -e

# Clone PokerStove repo
git clone https://github.com/andrewprock/pokerstove.git 
pokerstove-master

# Build it
cd pokerstove-master
mkdir -p build && cd build
cmake ..
make -j4

# Copy binary to root so Flask can use it
cp bin/ps-eval ../../ps-eval

