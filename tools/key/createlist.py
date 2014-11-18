#!/usr/bin/python2.6


s = ""
with open('./conf/accept.txt') as lines:
    for line in lines:
        a = line.strip('\r\n')
        s+=a+','
    print s
