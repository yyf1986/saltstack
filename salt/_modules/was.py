#!/usr/bin/python2.6

def psjava():
    cmd = "ps -ef | grep java |grep -vE 'grep|/bin/bash|/opt/logstash-1.4.1'"
    ret = __salt__['cmd.run'](cmd)
    return ret

def kill_3(pid):
    cmd = "kill -3 %s" % pid
    __salt__['cmd.run'](cmd)
    msg = "kill -3 %s sucess!" % pid
    return msg

def list():
    ret = ""
    try:
        prolfile_paths = __salt__['grains.item']('profile_info')['profile_info']
    except:
        prolfile_paths = "NULL"
    if prolfile_paths != "NULL" and prolfile_paths != "N/A":
        for profile_info in prolfile_paths.split(';'):
            profile = profile_info.split(':')[0]
            ret+=profile+"\r\n"
            cmd = "ls -l %s |grep -E 'javacore|heapdump'|awk '{print $NF}'" % profile
            ret+=__salt__['cmd.run'](cmd)+"\r\n"
    else:
        ret+="This minion can not find any profile."
    return ret

def getfile(path):
    ret = __salt__['cp.push'](path)
    return ret
