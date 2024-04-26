#!/bin/sh

echo "\n\n========================================"
echo "Show help guide: oricat --help"
oricat --help

echo "\n\n========================================"
echo "Run command with default config file: oricat"
oricat

echo "\n\n========================================"
echo "Run command with specified input output dirs:"
echo "oricat --input-dir fixtures/ --output-dir ../stage/"
oricat --input-dir fixtures/ --output-dir ../stage/
