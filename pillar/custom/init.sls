#!py
#coding:utf-8
import yaml
import os
 
def run():
    config = {}
    id = __opts__['id']
    pillar_root = __opts__['pillar_roots']['base'][0]
    path = '%s/custom/minions/%s' %(pillar_root,id)
    if os.path.isfile(path):
        s = open(path).read()
        config = yaml.load(s)
    else:
        pass
    return config
