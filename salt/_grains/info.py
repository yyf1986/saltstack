#!/usr/bin/python2.6

import os
import re
import httplib

def getinfo():
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
        systemmanager = ret.split(',')[3]
    else:
        systemname = "ERROR"
        systemenv = "ERROR"
        softtype = "ERROR"
        systemmanager = "ERROR"
    grains['systemname'] = systemname
    grains['systemenv'] = systemenv
    grains['softtype'] = softtype
    grains['systemmanager'] = systemmanager
    return grains
#getinfo()
