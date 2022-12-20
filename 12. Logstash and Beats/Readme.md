# Logstash

<img src="https://www.elastic.co/guide/en/logstash/7.17/static/images/logstash.png" alt="Logstash" height="250px" width="auto"/>

is an open source data collection engine
with real-time pipelining capabilities.
Logstash can dynamically unify data from
disparate sources and normalize the data
into destinations of your

### Concepts
The Logstash event processing pipeline has three stages: inputs → filters → outputs. Inputs generate 
events, filters modify them, and outputs ship them elsewhere. Inputs and outputs support codecs that 
enable you to encode or decode the data as it enters or exits the pipeline without having to use a separate 
filter.
The Logstash event processing pipeline coordinates the execution of inputs, filters, and outputs.
Each input stage in the Logstash pipeline runs in its own thread. Inputs write events to a central queue that 
is either in memory (default) or on disk. Each pipeline worker thread takes a batch of events off this queue, 
runs the batch of events through the configured filters, and then runs the filtered events through any 
outputs. The size of the batch and number of pipeline worker threads are configurable

### Input plugins
You use inputs to get data into Logstash. Some of the more commonly-used inputs are:
• file: reads from a file on the filesystem, much like the UNIX command tail -0F
• syslog: listens on the well-known port 514 for syslog messages and parses according to the RFC3164 
format
• redis: reads from a redis server, using both redis channels and redis lists. Redis is often used as a 
"broker" in a centralized Logstash installation, which queues Logstash events from remote Logstash 
"shippers".
There are many more input plugins available - https://www.elastic.co/guide/en/logstash/current/inputplugins.html

### Filter plugins
Filters are intermediary processing devices in the Logstash pipeline. You can combine filters with 
conditionals to perform an action on an event if it meets certain criteria. Some useful filters include:
• grok: parse and structure arbitrary text. Grok is currently the best way in Logstash to parse 
unstructured log data into something structured and queryable. With 120 patterns built-in to Logstash, 
it’s more than likely you’ll find one that meets your needs!
• mutate: perform general transformations on event fields. You can rename, remove, replace, and modify 
fields in your events.
• drop: drop an event completely, for example, debug events.
• clone: make a copy of an event, possibly adding or removing fields.
• geoip: add information about geographical location of IP addresses (also displays amazing charts in 
Kibana!)
There are many more filter plugins available - https://www.elastic.co/guide/en/logstash/current/filterplugins.html

### Output plugins
Outputs are the final phase of the Logstash pipeline. An event can pass through multiple outputs, but once 
all output processing is complete, the event has finished its execution. Some commonly used outputs 
include:
• elasticsearch: send event data to Elasticsearch. If you’re planning to save your data in an efficient, 
convenient, and easily queryable format…Elasticsearch is the way to go. Period. Yes, we’re biased :)
• file: write event data to a file on disk.
• graphite: send event data to graphite, a popular open source tool for storing and graphing metrics -
http://graphite.readthedocs.io/en/latest/
• statsd: send event data to statsd, a service that "listens for statistics, like counters and timers, sent 
over UDP and sends aggregates to one or more pluggable backend services". If you’re already using 
statsd, this could be useful for you!
There are many more output plugins available - https://www.elastic.co/guide/en/logstash/current/outputplugins.html

### Codecs
Codecs are basically stream filters that can operate as part of an input or output. Codecs enable you to 
easily separate the transport of your messages from the serialization process. Popular codecs 
include json, msgpack, and plain (text).
• json: encode or decode data in the JSON format.
• multiline: merge multiple-line text events such as java exception and stacktrace messages into a single 
event.
There are many more codec plugins available - https://www.elastic.co/guide/en/logstash/current/codecplugins.htm


# Beats

<img src="https://www.elastic.co/guide/en/beats/libbeat/current/images/beats-platform.png" alt="beats" height="250px" width="auto">

are open source data shippers that you
install as agents on your servers to send
different types of operational data
to Elasticsearch. Beats can send data
directly to Elasticsearch or send it to
Elasticsearch via Logstash, which you can
use to parse and transform the data.

### Metricbeat
Metricbeat is a lightweight shipper that you can install on your servers to periodically collect metrics from 
the operating system and from services running on the server. Metricbeat takes the metrics and statistics 
that it collects and ships them to the output that you specify. In our case, we will send this statistics 
directly to the Elasticsearch.
.
Metricbeat could work in conjunction with several services like PostgreSQL, Redis, MongoDB, MySQL, 
Windows, System and many others.
You could use System module. This module is enabled by default to collect metrics about your server, 
such as CPU usage, memory usage, network IO metrics, and process statistics