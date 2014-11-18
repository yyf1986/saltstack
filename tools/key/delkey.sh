#!/bin/bash
for ip in `cat ./conf/del.txt`; do
  echo $ip
  echo "Y"|salt-key -d $ip
done
