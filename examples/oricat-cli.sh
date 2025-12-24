#!/bin/sh
set -o errexit
set -o nounset

echo "\n\n========================================"
echo "Show help guide: oricat --help"
oricat --help

printf "\n\n========================================\n"
printf "Show version info: oricat --version\n"
oricat --version

echo "\n\n========================================"
echo "Prepare data"
mkdir -p ../stage/examples/input/
cp fixtures/categorise/*.* ../stage/examples/input/categorise/

echo "\n\n========================================"
echo "Run command with specified input output dirs:"
echo "oricat categorise --input-dir ../stage/examples/input/categorise/ --output-dir ../stage/output/categorise/"
oricat categorise --input-dir ../stage/examples/input/categorise/ --output-dir ../stage/output/categorise/
