#!/usr/bin/python2.6
# -*- coding: utf-8 -*-

import salt.key
import salt.client
import salt.config

def status():
    __opts__ = salt.config.client_config('/etc/salt/master')
    client = salt.client.LocalClient()
    minions = client.cmd('*', 'test.ping', timeout=30)

    key = salt.key.Key(__opts__)
    keys = key.list_keys()

    ret = {}
    ret['up'] = sorted(minions)
    ret['down'] = sorted(set(keys['minions']) - set(minions))
    return ret

print status().get('down')
#l1 = status().get('down')
#for d in l1:
    #print d
