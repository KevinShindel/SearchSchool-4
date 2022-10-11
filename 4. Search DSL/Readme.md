# Search API DSL

### use KIBANA DEVTOOLS for

- Query/aggregation editor with autocompletion
- Use it to compose small scenarios
- Alt-Enter to execute, check out „Help" for more shortcuts
- Session is persisted in browser cache

#### THE ENVELOPE

````json
{
  "query": {
    <--
    The
    queries
    go
    to
    the
    "query"
    section.
    "match_all": {}
    <--
    The
    query
    definition
  },
  "aggs": {
    <--
    The
    aggregations
    go
    to
    "aggs"
    (or
    "aggregations"
    )
    section
    "allTypes": {
      <--
      The
      aggregation
      name
      (
      "
      allTypes
      "
      )
      "terms": {
        "field": "type"
        <--
        The
        aggergation
        definition
      }
    }
  },
  "size": 10
  <--
  The
  max
  response
  size
  that
  should
  be
  returned
}
````

````json
{
  "query": {
    "match_all": {}
    <--
    Matches
    all
    documents
  }
}
````

#### IDS query

````json
{
  "query": {
    "ids": {
      "values": [
        "1",
        "4",
        "100"
      ]
    }
  }
}
````

### Search points

````text
POST /<index>/_search <--- Search in specified index
POST /<index1>,-<index2>/_search  <--- search in index and exclude index2
POST /<index1>,<index2>/_search  <--- search in multiple indexes
POST /<pattern>/_search  <--- Search in pattern index
POST /_all/_search  <--- Search in all indexes
````

### Term

````text
Term — the tokenized piece of text associated with the field name it belongs to e.g.: product:laptop (the "product" is the field name, the 
"laptop" is the value).
````

````json
{
  "text": "quick brown fox"
  <---
  Find
  inclusion
  quick
  |
  brown
  |
  fox
}
````

#### Terms query

````text
Like a single term query but you give it a list of 
searched for terms and it matches at documents 
with at least one of them.
If more than single term is matching to the same 
document property this document will be scored 
higher and will appear higher on the result list.
````

````json
{
  "query": {
    "terms": {
      "name": [
        "crisp",
        "resolution"
      ]
    }
  }
}
````

### RANGE QUERY

````text
As the name suggests – fetch the document with value in specific range.
The range can be string-based or number-based (and by the way — the date is a number!).
````

````json
{
  "query": {
    "range": {
      "regularPrice": {
        "gt": 200,
        "lte": 300
      }
    }
  }
}
````

````json
{
  "query": {
    "range": {
      "productSubclass": {
        "gte": "P",
        "lte": "R"
      }
    }
  }
}
````

#### RANGE QUERY — DATE MATH

````json
{
  "query": {
    "range": {
      "startDate": {
        "gte": "2013-07-14||+20M/M",
        "lte": "now-5m/M"
      }
    }
  }
}
````

#### PREFIX QUERY

- Matches the term by the provided prefix
- Note that the prefix text is not analyzed in this query. That means is while the data is upper-case and analyzed to be
  lower case you need to manually change the prefix to lowercase in order to match the document

````json
{
  "query": {
    "prefix": {
      "artist": "circ"
    }
  }
}
````

Results:

````json
{
  "artist": "A Perfect Circle",
  "votes": 200
}
````

#### REGEXP QUERY

- Functionality is pretty self-explanatory
- It is however limited when compared to the functionality of let’s say Java Pattern
- Be very careful with this query type — it can make your requests very slow easily

````json
{
  "query": {
    "regexp": {
      "name": {
        "value": ".*[Ll]isten(ing)?"
      }
    }
  }
}
````

#### BOOL QUERY

````json
{
  "bool": {
    "must": [],
    "filter": [],
    "must_not": [],
    "should": []
  }
}
````

# Mapping

#### Create

````text
PUT /demo_index
````

Data

````json
{
  "mappings": {
    "properties": {
      "age": {
        "type": "integer"
      },
      "email": {
        "type": "keyword"
      },
      "name": {
        "type": "text"
      }
    }
  }
}
````

#### Get mapping

````text
GET /demo_index/_mappings
````

````json
{
  "demo_index": {
    "mappings": {
      "properties": {
        "age": {
          "type": "integer"
        },
        "email": {
          "type": "keyword"
        },
        "name": {
          "type": "text"
        }
      }
    }
  }
}
````

### Add fields to existing mapping

````text
PUT /demo_index/_mappings
````

````json
{
  "properties": {
    "employee-id": {
      "type": "keyword",
      "index": false
    }
  }
}
````

````json
{
  "demo_index": {
    "mappings": {
      "properties": {
        "age": {
          "type": "integer"
        },
        "email": {
          "type": "keyword"
        },
        "employee-id": {
          "type": "keyword",
          "index": false
        },
        "name": {
          "type": "text"
        }
      }
    }
  }
}
````

### View specified field

````text
GET /my-index-000001/_mapping/field/employee-id
````

````json
{
  "demo_index": {
    "mappings": {
      "employee-id": {
        "full_name": "employee-id",
        "mapping": {
          "employee-id": {
            "type": "keyword",
            "index": false
          }
        }
      }
    }
  }
}
````

### Change value for specified doc
Method
````text
PUT /demo_index/_doc/1
````
DATA
````json
{
  "age": 30,
  "email": "kevin.shindel@yahoo.com",
  "employee-id": 1,
  "name": "Kevin Shindel"
}
````
Method
````text
POST /demo_index/_doc/1/_update
````
DATA
````json
{
    "doc": {
        "age": 40
        }
}
````
Result
````json
{
  "_index": "demo_index",
  "_type": "_doc",
  "_id": "1",
  "_version": 2,
  "_seq_no": 1,
  "_primary_term": 1,
  "found": true,
  "_source": {
    "age": 40,
    "email": "kevin.shindel@yahoo.com",
    "employee-id": 1,
    "name": "Kevin Shindel"
  }
}
````

### Update by Query
````text
POST /demo_index/_update_by_query
````
````json
{
    "query": {
        "term": {
            "age": 40
        }
    },
     "script": {
        "source": "ctx._source['email'] = 'demo@mail.com'"
  }
}
````

### Field types

````text
binary <--- Binary value encoded as a Base64 string.
boolean <--- true and false values.
Keywords <--- The keyword family, including keyword, constant_keyword, and wildcard.
Numbers <--- Numeric types, such as long and double, used to express amounts.
Dates <--- Date types, including date and date_nanos.
alias <--- Defines an alias for an existing field.
Objects and relational types
````

#### Object types
````text
object <--- A JSON object.
flattened <--- An entire JSON object as a single field value.
nested <---A JSON object that preserves the relationship between its subfields.
join <--- Defines a parent/child relationship for documents in the same index.
````

#### Structured data types
````text
Range <---Range types, such as long_range, double_range, date_range, and ip_range.
ip <--- IPv4 and IPv6 addresses.
version <--- Software versions. Supports Semantic Versioning precedence rules.
murmur3 <--- Compute and stores hashes of values.
````

#### Aggregate data type
````text
aggregate_metric_double <---Pre-aggregated metric values.
histogram <--- Pre-aggregated numerical values in the form of a histogram.
````
#### Text search types
````text
annotated-text <--- Text containing special markup. Used for identifying named entities.
completion <--- Used for auto-complete suggestions.
search_as_you_type <--- text-like type for as-you-type completion.
token_count <--- A count of tokens in a text.
````
#### Document ranking types
````text
dense_vector <--- Records dense vectors of float values.
rank_feature <--- Records a numeric feature to boost hits at query time.
rank_features <--- Records numeric features to boost hits at query time.
````
#### Spatial data types
````text
geo_point <--- Latitude and longitude points.
geo_shape <--- Complex shapes, such as polygons.
point <--- Arbitrary cartesian points.
shape <--- Arbitrary cartesian geometries.
````
#### Other types
````text
percolator <--- Indexes queries written in Query DSL.
````