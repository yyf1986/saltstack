#!/usr/bin/python

import salt.config
import salt.key


class AcceptKey():
    def __init__(self):
        pass
    def accept(self,ip):
        __opts__ = salt.config.client_config('/etc/salt/master')
        key = salt.key.Key(__opts__)
        keys = key.list_keys()
        minionpres = keys['minions_pre']
        if ip in minionpres:
            key.accept(ip)
            print "Add "+ip+" sucess!"
        else:
            print ip+" is not in minions_pre!"

with open('./conf/accept.txt') as lines:
    for line in lines:
        ip = line.strip('\r\n')
        #print ip
        ak = AcceptKey()
        ak.accept(ip)
