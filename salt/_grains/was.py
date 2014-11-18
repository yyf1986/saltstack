#!/usr/bin/python2.6
#-*- coding: utf-8 -*-

import os
import re
import httplib

def discoverywas():
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
    if softtype == "WAS":
        cmd = "ps -ef | grep java | grep 'IBM/WebSphere/AppServer'|grep -v grep|grep -v 'sh -c'|awk '{print $1}'|sort|uniq|wc -l"
        user_num = os.popen(cmd).readlines()[0].strip('\r\n')
        if int(user_num) == 1:
            cmd = "ps -ef | grep java | grep 'IBM/WebSphere/AppServer'|grep -v grep|grep -v 'sh -c'|awk '{print $1}'|sort|uniq"
            was_user = os.popen(cmd).readlines()[0].strip('\r\n')
            grains['was_user'] = was_user
        else:
            grains['was_user'] = "ERROR"
        #通过判断进程的最后一个是否是dmgr来判断是否是dmgr
        cmd = "ps -ef|grep java|grep 'IBM/WebSphere/AppServer'|grep dmgr|grep -v grep|grep -v 'sh -c'|awk '{if($NF == \"dmgr\") print $0}'|wc -l"
        dmgr_pid_num = os.popen(cmd).readlines()[0].strip('\r\n')
        if int(dmgr_pid_num) == 1:
            cmd = "ps -ef | grep java|grep 'IBM/WebSphere/AppServer'|grep -v grep|grep -v 'sh -c'|grep dmgr|awk '{if($NF == \"dmgr\") print $0}'|awk '{for(i=1;i<=NF;i++){if($i ~ \"^-Dserver.root\")print $i}}'|awk -F '=' '{print $2}'"
            dmgr_path = os.popen(cmd).readlines()[0].strip('\r\n')
            grains['dmgr_path'] = dmgr_path
            #在是dmgr的前提下，通过判断nodeagent的进程数
            cmd = "ps -ef | grep java|grep -v grep|grep nodeagent|grep -v 'sh -c'|awk '{for(i=1;i<=NF;i++){if($i ~ \"^-Dserver.root\")print $i}}'|awk -F '=' '{print $2}'|uniq|wc -l"
            node_num = os.popen(cmd).readlines()[0].strip('\r\n')
            #支持多node
            if int(node_num) >= 1:
                li = []
                cmd = "ps -ef | grep java|grep -v grep|grep nodeagent|grep -v 'sh -c'|awk '{for(i=1;i<=NF;i++){if($i ~ \"^-Dserver.root\")print $i}}'|awk -F '=' '{print $2}'|uniq"
                profile_paths = os.popen(cmd).readlines()
                for profile_path in profile_paths:
                    profile_info = profile_path.strip('\r\n')+':'
                    logpath = profile_path.strip('\r\n')+"/logs"
                    files = os.listdir(logpath)
                    for file in files:
                        if os.path.isdir(logpath+"/"+file):
                            if file not in ['ffdc','nodeagent']:
                                if os.path.isfile(logpath+"/"+file+"/SystemOut.log"):
                                    profile_info+=file+","
                                else:
                                    pass
                            else:
                                pass
                        else:
                            pass
                    profile_info = re.sub(',$','',profile_info)
                    li.append(profile_info)
                profile_info = ""
                for i in range(0,len(li)):
                    profile_info+=li[i]+';'
                #多个profile以分号分隔
                profile_info = re.sub(';$','',profile_info)
                grains['profile_info'] = profile_info
            #如果没有nodeagent，判断有没was的进程，如果有为standalone
            else:
                cmd = "ps -ef | grep java|grep 'IBM/WebSphere/AppServer'|grep -v grep|grep -v 'sh -c'|awk '{if($NF != \"dmgr\") print $0}'|wc -l"
                java_pid_num = os.popen(cmd).readlines()[0].strip('\r\n')
                if int(java_pid_num) >= 1:
                    li = []
                    cmd = "ps -ef | grep java|grep 'IBM/WebSphere/AppServer'|grep -v grep|grep -v 'sh -c'|awk '{if($NF != \"dmgr\") print $0}'|awk '{for(i=1;i<=NF;i++){if($i ~ \"^-Dserver.root\")print $i}}'|awk -F '=' '{print $2}'|uniq"
                    profile_paths = os.popen(cmd).readlines()
                    for profile_path in profile_paths:
                        profile_info = profile_path.strip('\r\n')+':'
                        logpath = profile_path.strip('\r\n')+"/logs"
                        files = os.listdir(logpath)
                        for file in files:
                            if os.path.isdir(logpath+"/"+file):
                                if file not in ['ffdc','nodeagent']:
                                    if os.path.isfile(logpath+"/"+file+"/SystemOut.log"):
                                        profile_info+=file+","
                                    else:
                                        pass
                                else:
                                    pass
                            else:
                                pass
                        profile_info = re.sub(',$','',profile_info)
                        li.append(profile_info)
                    profile_info = ""
                    for i in range(0,len(li)):
                        profile_info+=li[i]+';'
                    #多个profile以分号分隔
                    profile_info = re.sub(';$','',profile_info)
                    grains['profile_info'] = profile_info
                else:
                    grains['profile_info'] = "N/A"
        elif int(dmgr_pid_num) == 0:
            grains['dmgr_path'] = "N/A"
            cmd = "ps -ef | grep java|grep 'IBM/WebSphere/AppServer'|grep -v grep|grep 'nodeagent'|grep -v 'sh -c'|wc -l"
            nodenum = os.popen(cmd).readlines()[0].strip('\r\n')
            #如果不是dmgr，判断nodeagent
            if int(nodenum) >= 1:
                li = []
                cmd = "ps -ef | grep java|grep 'IBM/WebSphere/AppServer'|grep -v grep|grep nodeagent|grep -v 'sh -c'|awk '{for(i=1;i<=NF;i++){if($i ~ \"^-Dserver.root\")print $i}}'|awk -F '=' '{print $2}'|uniq"
                profile_paths = os.popen(cmd).readlines()
                for profile_path in profile_paths:
                    profile_info = profile_path.strip('\r\n')+':'
                    logpath = profile_path.strip('\r\n')+"/logs"
                    files = os.listdir(logpath)
                    for file in files:
                        if os.path.isdir(logpath+"/"+file):
                            if file not in ['ffdc','nodeagent']:
                                if os.path.isfile(logpath+"/"+file+"/SystemOut.log"):
                                    profile_info+=file+","
                                else:
                                    pass
                            else:
                                pass
                        else:
                            pass
                    profile_info = re.sub(',$','',profile_info)
                    li.append(profile_info)
                profile_info = ""
                for i in range(0,len(li)):
                    profile_info+=li[i]+';'
                #多个profile以分号分隔
                profile_info = re.sub(';$','',profile_info)
                grains['profile_info'] = profile_info
            #如果没有nodeagent，判断有没was的进程，如果有为standalone
            else:
                cmd = "ps -ef | grep java|grep 'IBM/WebSphere/AppServer'|grep -v grep|grep -v 'sh -c'|wc -l"
                java_pid_num = os.popen(cmd).readlines()[0].strip('\r\n')
                if int(java_pid_num) >= 1:
                    li = []
                    cmd = "ps -ef | grep java|grep 'IBM/WebSphere/AppServer'|grep -v grep|grep -v 'sh -c'|awk '{for(i=1;i<=NF;i++){if($i ~ \"^-Dserver.root\")print $i}}'|awk -F '=' '{print $2}'|uniq"
                    profile_paths = os.popen(cmd).readlines()
                    for profile_path in profile_paths:
                        profile_info = profile_path.strip('\r\n')+':'
                        logpath = profile_path.strip('\r\n')+"/logs"
                        files = os.listdir(logpath)
                        for file in files:
                            if os.path.isdir(logpath+"/"+file):
                                if file not in ['ffdc','nodeagent']:
                                    if os.path.isfile(logpath+"/"+file+"/SystemOut.log"):
                                        profile_info+=file+","
                                    else:
                                        pass
                                else:
                                    pass
                            else:
                                pass
                        profile_info = re.sub(',$','',profile_info)
                        li.append(profile_info)
                    profile_info = ""
                    for i in range(0,len(li)):
                        profile_info+=li[i]+';'
                    #多个profile以分号分隔
                    profile_info = re.sub(';$','',profile_info)
                    grains['profile_info'] = profile_info
                else:
                    grains['profile_info'] = "N/A"
        else:
            pass
    else:
        pass
    return grains
#discoverywas()
