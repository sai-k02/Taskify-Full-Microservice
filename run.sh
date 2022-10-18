#!/bin/bash

cd main
# get data
/usr/local/go/bin/go run . 
# upload data
/Library/Frameworks/Python.framework/Versions/3.9/bin/python3 TaskController.py $1
