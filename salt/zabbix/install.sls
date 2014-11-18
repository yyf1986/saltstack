{% if grains['os_family'] == "RedHat" %}
zabbix:
  pkg:
    - installed
zabbix-agent:
  pkg:
    - installed
    - require:
      - pkg: zabbix
  service:
    - running
    - enable: True
    - require:
      - pkg: zabbix-agent
{% elif grains['os_family'] == "Suse" %}
zabbix-agent:
  pkg:
    - installed
zabbix-agentd:
  service:
    - running
    - enable: True
    - require:
      - pkg: zabbix-agent
{% endif %}
  file.managed:
{% if grains['os_family'] == "RedHat" %}
    - name: /etc/zabbix/zabbix_agentd.conf
    - source: salt://zabbix/conf/zabbix_agentd.conf
{% elif grains['os_family'] == "Suse" %}
    - name: /etc/zabbix/zabbix-agentd.conf
    - source: salt://zabbix/conf/zabbix-agentd.conf
{% endif %}
    - user: root
    - mode: 644
    - require:
      - pkg: zabbix-agent
modfiy1:
  file.sed:
{% if grains['os_family'] == "RedHat" %}
    - name: /etc/zabbix/zabbix_agentd.conf
{% elif grains['os_family'] == "Suse" %}
    - name: /etc/zabbix/zabbix-agentd.conf
{% endif %}
    - before: Hostname=
    - after: Hostname={{ grains['id'] }}
    - require:
      - pkg: zabbix-agent
modfiy2:
  file.sed:
{% if grains['os_family'] == "RedHat" %}
    - name: /etc/zabbix/zabbix_agentd.conf
{% elif grains['os_family'] == "Suse" %}
    - name: /etc/zabbix/zabbix-agentd.conf
{% endif %}
    - before: ServerActive=
    - after: ServerActive={{ grains['zabbix_proxy'] }}
    - require:
      - pkg: zabbix-agent
scpconf:
  file.recurse:
    - name: /etc/zabbix/zabbix_agentd.d
    - source: salt://zabbix/zabbix_agentd.d
    - clean: True
    - require:
      - pkg: zabbix-agent
scpscript:
  file.recurse:
    - name: /opt/zabbix/lldscripts
    - source: salt://zabbix/lldscripts
    - clean: True
    - require:
      - pkg: zabbix-agent
{% if salt['cmd.run']("grep 'zabbix' /etc/sudoers|wc -l") != "2" %}
addsudoers:
  cmd.run:
    - name: echo 'Defaults:zabbix !requiretty' >> /etc/sudoers;echo 'zabbix ALL=(root) NOPASSWD:/home/mysql/bin/mysql,/home/mysql/bin/mysqladmin,/sbin/lvdisplay,/usr/sbin/lvdisplay,/bin/netstat,/bin/sh,/bin/sh,/usr/sbin/lsof' >> /etc/sudoers
    - require:
      - pkg: zabbix-agent
{% endif %}
{% if salt['cmd.run']("ps -ef | grep /home/mysql/bin/mysqld|grep -v grep|wc -l") != "0" %}
perl-libwww-perl:
  pkg:
    - installed
perl-Crypt-SSLeay:
  pkg:
    - installed
perl-Digest-SHA:
  pkg:
    - installed
perl-DBD-MySQL:
  pkg:
    - installed
perl-File-Which:
  pkg:
    - installed
zabbix-sender:
  pkg:
    - installed
modifyconf1:
  file.sed:
    - name: /opt/zabbix/lldscripts/fromdual_mysql/etc/FromDualMySQLagent.conf
    - before: 10.27.38.201
    - after: {{ grains['id'] }}
    - require:
      - pkg: perl-libwww-perl
      - pkg: perl-Crypt-SSLeay
      - pkg: perl-Digest-SHA
      - pkg: perl-DBD-MySQL
      - pkg: perl-File-Which
      - pkg: zabbix-sender
modifyconf2:
  file.sed:
    - name: /opt/zabbix/lldscripts/fromdual_mysql/etc/FromDualMySQLagent.conf
    - before: ZabbixServer = 192.168.90.18
    - after: ZabbixServer = {{ grains['zabbix_proxy'] }}
    - require:
      - pkg: perl-libwww-perl
      - pkg: perl-Crypt-SSLeay
      - pkg: perl-Digest-SHA
      - pkg: perl-DBD-MySQL
      - pkg: perl-File-Which
      - pkg: zabbix-sender
changemode:
  cmd.run:
    - name: chown -R zabbix.zabbix zabbix;chmod 755 /opt/zabbix/lldscripts/fromdual_mysql/FromDualMySQLagent.pl
    - cwd: /opt/
    - watch:
      - file: /opt/zabbix/lldscripts/fromdual_mysql/etc/FromDualMySQLagent.conf
{% endif %}
restart:
  cmd.run:
{% if grains['os_family'] == "RedHat" %}
    - name: /etc/init.d/zabbix-agent restart
{% elif grains['os_family'] == "Suse" %}
    - name: /etc/init.d/zabbix-agentd restart
{% endif %}
    - require:
      - pkg: zabbix-agent
