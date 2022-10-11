# Indexing

### Inverted index 
````text
An inverted index is an index
data structure storing a
mapping from content, such as
words or numbers, to its
locations in a document or a
set of documents. In simple
words, it is a hashmap like
data structure that directs you
from a word to a document or
a web page.




````

### COMPARISON TO RDBMS TABLE

````text
+------------------------------------------------+
+--Relational Databases-----------Inverted index-+
+================================================+
+---Database----------------------Index----------+
+---Table-------------------------Type-----------+
+---Row---------------------------Document-------+
+---Column------------------------Fields---------+
+---Schema------------------------Mapping--------+
+------------------------------------------------+
````
### <a href="https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-put-mapping.html">Mapping</a>

#### Create a new index with mapping

````text
PUT /publications

PUT /publications/_mapping
{
  "properties": {
    "title":  { "type": "text"}
  }
}
````


#### Create multiple mappings
````text

# Create the two indices
curl -X PUT "localhost:9200/my-index-000001?pretty"
curl -X PUT "localhost:9200/my-index-000002?pretty"
# Update both mappings
curl -X PUT "localhost:9200/my-index-000001,my-index-000002/_mapping?pretty" -H 'Content-Type: application/json' -d'
{
  "properties": {
    "user": {
      "properties": {
        "name": {
          "type": "keyword"
        }
      }
    }
  }
}
'
````


#### Update mapping API

````text
PUT /my-index-000001/_mapping
{
  "properties": {
    "email": {
      "type": "keyword"
    }
  }
}
````

#### Add new properties to an existing object 
````text
curl -X PUT "localhost:9200/my-index-000001?pretty" -H 'Content-Type: application/json' -d'
{
  "mappings": {
    "properties": {
      "name": {
        "properties": {
          "first": {
            "type": "text"
          }
        }
      }
    }
  }
}
'

curl -X PUT "localhost:9200/my-index-000001/_mapping?pretty" -H 'Content-Type: application/json' -d'
{
  "properties": {
    "name": {
      "properties": {
        "last": {
          "type": "text"
        }
      }
    }
  }
}
'

````