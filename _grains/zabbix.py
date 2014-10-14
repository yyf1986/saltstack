#!/usr/bin/python
import random
import os

def zabbixproxy():
    cmd = "ifconfig|grep Bcast|awk '{print $2}'|cut -d ':' -f2"
    ip = os.popen(cmd).readlines()[0].strip('\r\n')
    ips = ["192.168.90.18","192.168.90.20","192.168.90.21","192.168.90.23","192.168.90.25","192.168.90.28",'192.168.90.26']
    zabbix_conf="/etc/zabbix/zabbix_agentd.conf"
    grains = {}
    if ip not in ips:
        if os.path.exists(zabbix_conf):
            with open(zabbix_conf) as lines:
                for line in lines:
                    if line.startswith('ServerActive'):
                        ip = line.split('=')[1].strip('\r\n')
                        try:
                            num = ips.index(ip, )
                            proxy_ip = ip
                        except:
                            num = -1
                            for j in random.sample([0,1,2,3,4,5,6],1):
                                proxy_ip = ips[j]
                        grains['zabbix_proxy'] = proxy_ip
                    else:
                        pass
        else:
            for j in random.sample([0,1,2,3,4,5],1):
                proxy_ip = ips[j]
            grains['zabbix_proxy'] = proxy_ip
    else:
        grains['zabbix_proxy'] = "zabbix_proxy"
    return grains
