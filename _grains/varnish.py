#!/usr/bin/python2.6

import os
import re
import httplib

def discoveryvarnish():
    grains = {}
    cmd = "ifconfig|grep Bcast|awk '{print $2}'|cut -d ':' -f2"
    ip = os.popen(cmd).readlines()[0].strip('\r\n')
    url = "yunwei/api/IptoSysEname.do?ip="+ip
    try:
        conns = httplib.HTTPConnection("192.168.224.36",80,True,5)
        if not url.startswith('/'):
            url="/"+url
        conns.request("GET",url)
        response = conns.getresponse()
        ret = response.read()
    except Exception:
        ret = "N-connect"
    finally:
        conns.close()
    if str(ret) != "N-connect":
        systemname = ret.split(',')[0]
        systemenv = ret.split(',')[1]
        softtype = ret.split(',')[2]
    else:
        systemname = "ERROR"
        systemenv = "ERROR"
        softtype = "ERROR"
    grains['systemname'] = systemname
    grains['systemenv'] = systemenv
    grains['softtype'] = softtype
    if softtype.lower() == "varnish":
        cmd = "ps -ef | grep varnish|grep /usr/sbin/rotatelogs|grep -E 'varnish_log|varnishstat_log'|grep -v 'sh -c'|wc -l"
        log_pid = os.popen(cmd).readlines()[0].strip('\r\n')
        if int(log_pid) >= 1:
            cmd = "ps -ef | grep varnish|grep /usr/sbin/rotatelogs|grep -E 'varnish_log|varnishstat_log'|grep -v 'sh -c'|awk '{print $(NF - 2)}'|sed -e 's/\/varnish_log.*$//' -e 's/\/varnishstat_log_.*$//'|uniq"
            varnish_log_path = os.popen(cmd).readlines()[0].strip('\r\n')
            grains['varnish_log_path'] = varnish_log_path
        else:
           grains['varnish_log_path'] = "N/A" 
    else:
        pass
    return grains
#discoveryvarnish()
