#!/bin/bash

THIS_DIR=$(dirname $0)
echo $THIS_DIR
EINGANG_DIR="$($THIS_DIR/python -m eingang.Eingang)"
echo $EINGANG_DIR
cp $EINGANG_DIR/Makefile .
