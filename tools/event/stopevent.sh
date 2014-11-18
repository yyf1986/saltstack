#!/bin/bash
ps -ef | grep event.py|grep -v grep |awk '{print $2}'|xargs -I {} kill -9 {}
