#!/usr/bin/python
import salt.client

class Run():
    def __init__(self):
        pass
    def run(self):
        local = salt.client.LocalClient()
        ret = local.cmd('*','cmd.run',["ps -ef | grep zabbix|grep -v grep |grep -v 'sh -c'|wc -l"])
        #ret = local.cmd('proxy1','cmd.run',["ps -ef | grep zabbix|grep -v grep |grep -v 'sh -c'|wc -l"],expr_form='nodegroup')
        for key,value in ret.items():
            if int(value) == 2:
                print key
r = Run()
r.run()
