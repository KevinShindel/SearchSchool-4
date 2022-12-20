FROM logstash:6.4.0
ADD /config/http-pipeline.conf /usr/share/logstash/config
ADD /config/logstash.yml /usr/share/logstash/config
CMD logstash -f /usr/share/logstash/config/http-pipeline.conf