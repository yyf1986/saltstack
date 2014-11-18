{% if salt['cmd.run']("cd /opt/;ls -l|grep -w logstash-1.4.1|wc -l") == "0" %}
logstash:
  pkg:
    - installed
permission:
  cmd.run:
    - name: chmod -R 755 *
    - cwd: /opt/logstash-1.4.1/
    - unless: ps -ef | grep logstash-1.4.1|grep -v grep
    - require:
      - pkg: logstash
createconf:
  cmd.run:
{% if grains['softtype'] == "WAS" %}
    - name: ./logstash.sh {{ grains['id'] }} {{ grains['systemname'] }} {{ grains['softtype']}} {{ grains['profile_info'] }}
{% elif grains['softtype'] == "IHS" %}
    - name: ./logstash.sh {{ grains['id'] }} {{ grains['systemname'] }} {{ grains['softtype']}} {{ grains['ihs_log_path'] }}
{% elif grains['softtype'] == "Varnish" %}
    - name: ./logstash.sh {{ grains['id'] }} {{ grains['systemname'] }} {{ grains['softtype']}} {{ grains['varnish_log_path'] }}
{% elif grains['softtype'] == "NULL" %}
    - name: ./logstash.sh {{ grains['id'] }} N/A N/A N/A
{% endif %}
    - cwd: /opt/logstash-1.4.1/bin
    - timeout: 10
    - unless: ps -ef | grep logstash-1.4.1|grep -v grep 
    - require:
      - pkg: logstash
modify:
  file.sed:
    - name: /opt/logstash-1.4.1/bin/shipper.conf
    - before: \@REDIS\@
    - after: 192.168.55.70
    - require:
      - pkg: logstash
start:
  cmd.run:
    - name: ./app.sh start
    - cwd: /opt/logstash-1.4.1/bin
    - timeout: 10
    - unless: ps -ef | grep logstash-1.4.1|grep -v grep
    - watch:
      - file: /opt/logstash-1.4.1/bin/shipper.conf
check:
  cmd.run:
    - name: ps -ef | grep logstash-1.4.1|grep -v grep
{% endif %}
