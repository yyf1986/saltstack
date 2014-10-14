#!/usr/bin/python2.6

import os
import re
import httplib

def discoveryihs():
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
    if softtype == "IHS":
        cmd = "ps -ef | grep httpd|grep IBM|grep -v 'grep|admin.conf'|grep -v '/opt/flume'|wc -l"
        httpd_num = os.popen(cmd).readlines()[0].strip('\r\n')
        if int(httpd_num) >= 1:
            cmd = "cd /proc/`ps -ef | grep httpd|grep IBM|grep -v admin.conf|grep -v '/opt/flume'|awk '{if($3 == \"1\")print $2}'`;ls -l|grep exe|awk '{print $NF}'|sed -e 's/\/httpd//'"
            ihs_bin = os.popen(cmd).readlines()[0].strip('\r\n')
            grains['ihs_bin'] = ihs_bin
            cmd = "ps -ef |grep http |grep IBM|grep -v admin.conf|grep -v '/opt/flume'|awk '{if($3 == \"1\")print $0}'|awk '{for(i=1;i<=NF;i++){if ($i ~ \".conf\")print $i}}'"
            ihs_config = os.popen(cmd).readlines()
            if len(ihs_config) == 0:
                grains['ihs_config_file'] = "N/A"
                grains['ihs_log_path'] = "N/A"
            else: 
                ihs_config_file = ihs_config[0].strip('\r\n')
                grains['ihs_config_file'] = ihs_config_file
                cmd = "grep ^CustomLog "+ihs_config_file+"|grep combined5|grep "+ihs_bin+"|wc -l"
                ihs_log_flag = os.popen(cmd).readlines()[0].strip('\r\n')
                if int(ihs_log_flag) != 1:
                    grains['ihs_log_path'] = "N/A"
                else:
                    cmd = "grep ^CustomLog "+ihs_config_file+"|awk '{print $4}'|sed -e 's/\/access.*$//'"
                    ihs_log_path = os.popen(cmd).readlines()[0].strip('\r\n')
                    grains['ihs_log_path'] = ihs_log_path
        else:
            grains['ihs_bin'] = "N/A"
            grains['ihs_config_file'] = "N/A"
            grains['ihs_log_path'] = "N/A"
    else:
        pass
    return grains
#discoveryihs()
