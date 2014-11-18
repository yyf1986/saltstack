#!/usr/bin/python

import salt.config
import salt.utils.event
import log

__opts__ = salt.config.client_config('/etc/salt/master')
loger = log.Log("salt")
loger.set_Path('./logs/')
event = salt.utils.event.MasterEvent(__opts__['sock_dir'])
for eachevent in event.iter_events(full=True):
    ret = eachevent['data']
    if "salt/job/" in eachevent['tag']:
        if ret.has_key('id') and ret.has_key('return'):
            if ret['fun'] == "saltutil.find_job":
                continue
            try:
                msg = str(ret['jid'])+" "+str(ret['id'])+" "+str(ret['fun'])+" "+str(ret['fun_args'])+" "+str(ret['retcode'])+" "+str(ret['success'])
                loger.set_Level("info")
            except:
                msg = ret
            if str(ret['success']) != "True" or int(ret['retcode']) != 0:
                loger.set_Level("error")
            loger.set_Name("msg")
            loger.add_Msg(msg)
    elif "salt/auth" in eachevent['tag']:
        try:
            msg = str(ret['_stamp'])+" "+str(ret['act'])+" "+str(ret['id'])+" "+str(ret['result'])
            loger.set_Level("info")
        except:
            msg = ret
        if str(ret['result']) != "True":
            loger.set_Level("error")
        loger.set_Name("auth")
        loger.add_Msg(msg)
    elif "new_job" in eachevent['tag']:
        msg = str(ret['tgt_type'])+" "+str(ret['jid'])+" "+str(ret['tgt'])+" "+str(ret['user'])+" "+str(ret['fun'])+" "+str(ret['arg'])+" "+str(ret['minions'])
        loger.set_Name("job")
        loger.add_Msg(msg)
    else:
        pass
