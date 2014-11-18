#!/usr/bin/python2.6
import os
import time
def stop():
    try:
        ihs_bin = __grains__['ihs_bin']
        ihs_config_file = __grains__['ihs_config_file']
    except:
        ihs_bin = "NULL"
        ihs_config_file = "NULL"
    if ihs_bin.endswith('bin'):
        cmd = "ps -ef | grep httpd |grep -Ev 'flume|grep' |grep -v '/bin/bash'|wc -l"
        pid_num = __salt__['cmd.run'](cmd)
        if int(pid_num) > 2:
            cmd = ihs_bin+"/apachectl -k stop -f "+ihs_config_file
            __salt__['cmd.run'](cmd)
            cmd = "ps -ef | grep httpd |grep -Ev 'flume|grep' |grep -v '/bin/bash'|grep -v '[httpd] <defunct>'|wc -l"
            pid_num = __salt__['cmd.run'](cmd)
            if int(pid_num) <= 3:
               msg = "IHS stop sucess!"
            else:
               msg = "IHS stop fail!"
        elif int(pid_num) == 0:
            msg = "IHS is not running!"
    else:
        msg = "IHS is not installed!"
    return msg

def start():
    try:
        ihs_bin = __grains__['ihs_bin']
        ihs_config_file = __grains__['ihs_config_file']
    except:
        ihs_bin = "NULL"
        ihs_config_file = "NULL"
    if ihs_bin.endswith('bin'):
        cmd = "ps -ef | grep httpd |grep -Ev 'flume|grep' |grep -v '/bin/bash'|wc -l"
        pid_num = __salt__['cmd.run'](cmd)
        if int(pid_num) == 0:
            cmd = ihs_bin+"/apachectl -k start -f "+ihs_config_file
            __salt__['cmd.run'](cmd)
            cmd = "ps -ef | grep httpd |grep -Ev 'flume|grep' |grep -v '/bin/bash'|wc -l"
            pid_num = __salt__['cmd.run'](cmd)
            if int(pid_num) >= 1:
                msg = "IHS start sucess!"
            else:
                msg =  "IHS start fail!"
        elif int(pid_num) > 3:
            msg = "IHS is running!"
    else:
        msg = "IHS is not installed!"
    return msg

def status():
    try:
        ihs_bin = __grains__['ihs_bin']
        ihs_config_file = __grains__['ihs_config_file']
    except:
        ihs_bin = "NULL"
        ihs_config_file = "NULL"
    if ihs_bin.endswith('bin'):
        pid_cmd = "ps -ef | grep httpd |grep -Ev 'flume|grep' |grep -v '/bin/bash'|wc -l"
        pid_num = __salt__['cmd.run'](pid_cmd)
        if int(pid_num) > 2:
            return "IHS is running!"
        elif int(pid_num) == 0:
            return "IHS is not running!"
    else:
        return "IHS is not installed!"
