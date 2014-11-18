#!/usr/bin/python2.6

def psjava():
    cmd = "ps -ef | grep java |grep -vE 'grep|/bin/bash|/opt/logstash-1.4.1'"
    ret = __salt__['cmd.run'](cmd)
    return ret

def jstack32(pid,path):
    cmd = "cd /opt/jboss/java32/jdk1.7.0_25/bin/;./jstack %s > %s" % (pid,path)
    __salt__['cmd.run'](cmd)
    msg = "jstack %s sucess!" % pid
    return msg

def jstack64(pid,path):
    cmd = "cd /opt/jboss/java64/jdk1.7.0_25/bin/;./jstack %s > %s" % (pid,path)
    __salt__['cmd.run'](cmd)
    msg = "jstack %s sucess!" % pid
    return msg 

def jmap32(pid,path):
    cmd = "cd /opt/jboss/java32/jdk1.7.0_25/bin/;./jmap -dump:format=b,file=%s %s" % (path,pid)
    __salt__['cmd.run'](cmd)
    msg = "jstack %s sucess!" % pid
    return msg

def jmap64(pid,path):
    cmd = "cd /opt/jboss/java64/jdk1.7.0_25/bin/;./jmap -dump:format=b,file=%s %s" % (path,pid)
    __salt__['cmd.run'](cmd)
    msg = "jstack %s sucess!" % pid
    return msg

def getfile(path):
    ret = __salt__['cp.push'](path)
    return ret
