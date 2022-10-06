# Installation of Elasticsearch+Kibana

Description
How to run it?

Presentation: 3. Installation of Elasticsearch+Kibana, how to run it.pdf

Useful links:

Set up Elasticsearch:https://www.elastic.co/guide/en/elasticsearch/reference/current/setup.html

Installing Elasticsearch: https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html

Configure Kibana: https://www.elastic.co/guide/en/kibana/current/settings.html

How to explore sample data: https://www.elastic.co/guide/en/kibana/7.11/get-started.html#gs-get-data-into-kibana

<hr/>

### Install On-demand

````shell
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.4.3-linux-x86_64.tar.gz
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.4.3-linux-x86_64.tar.gz.sha512
shasum -a 512 -c elasticsearch-8.4.3-linux-x86_64.tar.gz.sha512
tar -xzf elasticsearch-8.4.3-linux-x86_64.tar.gz
cd elasticsearch-8.4.3/ 
./bin/elasticsearch
````

### Install Elasticsearch by Docker
Obtaining Elasticsearch for Docker is as simple as issuing a docker pull command against the Elastic Docker registry.
````shell
  docker pull docker.elastic.co/elasticsearch/elasticsearch:8.4.3
  docker network create elastic
  docker run -d --name es01 \ 
           --net elastic \ 
           -p 9200:9200 -p 9300:9300 \
           docker.elastic.co/elasticsearch/elasticsearch:8.4.3
````

````text
If you need to reset the password for the elastic user or other built-in users, run the
elasticsearch-reset-password tool. This tool is available in the Elasticsearch /bin directory 
of the Docker container. For example:
````
````shell
docker exec -it es01 /usr/share/elasticsearch/bin/elasticsearch-reset-password
````

````text
Copy the http_ca.crt security certificate from your Docker container to your local machine.
````
````shell
docker cp es01:/usr/share/elasticsearch/config/certs/http_ca.crt .
````

#### Open a new terminal and verify that you can connect to your Elasticsearch cluster by making an authenticated call,
using the http_ca.crt file that you copied from your Docker container. Enter the password for the elastic user when prompted.
````shell
curl --cacert http_ca.crt -u elastic https://localhost:9200
````
