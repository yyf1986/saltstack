#!/usr/bin/python

import salt.config
import salt.utils.event
import salt.key
import salt.output
__opts__ = salt.config.client_config('/etc/salt/master')
key = salt.key.Key(__opts__)
keys = key.list_keys()
#print keys
minionnum = len(keys['minions'])
minionprenum = len(keys['minions_pre'])
print minionnum,minionprenum
s = ""
i = 1
#for m in  keys['minions']:
   #print m
    #print i,m
    #s+=m+","
    #if i == 1200:
    #    break
    #i = i + 1
#print s
#keycli = salt.key.KeyCLI(__opts__)
#print keycli.list_all()
#print keycli.list_status("pre")
#keycli.reject_all()
#print keycli.list_status("pre")
