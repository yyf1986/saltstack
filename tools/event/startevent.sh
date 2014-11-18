#!/bin/bash
bin=`dirname $0`
cd $bin
nohup python event.py > ./logs/error.log 2>&1 &
