#!/bin/sh

echo "\n\n========================================"
echo "Show help guide: oricat --help"
oricat --help

echo "\n\n========================================"
echo "Prepare data"
mkdir -p ../stage/examples/input/
cp fixtures/*.* ../stage/examples/input/

echo "\n\n========================================"
echo "Run command with specified input output dirs:"
echo "oricat --input-dir ../stage/examples/input/ --output-dir ../stage/output/"
oricat --input-dir ../stage/examples/input/ --output-dir ../stage/examples/output/
