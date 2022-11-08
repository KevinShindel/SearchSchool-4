# Aggregations

An aggregation summarizes your data as metrics, statistics, or other type of analytics.
It could help to answer such questions as:
- What’s the average load time for my website?
- Who are my most valuable customer?
- What would be considered a large file on my network?
- How many products are in each product category?

## TYPES:
There are many types of aggregations, but Elasticsearch organizes them into three categories:
- Metric Calculate metrics, such as a sum of average, from field values.
- Bucket Group documents into buckets, based on field values, ranges, or other criteria. Terms aggregation, 
for example.
- Pipeline Take input from other aggregations instead of documents

## SIMPLE EXAMPLE

````text
GET /my-index-000001/_search
{
  "aggs": {
    "my-agg-name": {
      "terms": {
        "field": "my-field"
      }
    }
  }
}
````

````json
{
  "took": 78,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 5,
      "relation": "eq"
    },
    "max_score": 1.0,
    "hits": [...]
  },
  "aggregations": {
    "my-agg-name": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": []
    }
  }
}
````

## SCOPE

````text
GET /my-index-000001/_search
{
  "query": { --> You could use query parameter to limit the documents on which aggregation runs
    "range": {
      "@timestamp": {
        "gte": "now-1d/d",
        "lt": "now/d"
      }
    }
  },
  "aggs": {
    "my-agg-name": {
      "terms": {
        "field": "my-field"
      }
    }
  }
}
````

## SIZE 

````text
GET /my-index-000001/_search
{
  "size": 0, --> You could return only aggregation results, by setting size to 0
  "aggs": {
    "my-agg-name": {
      "terms": {
        "field": "my-field"
      }
    }
  }
}
````

## MULTIPLE AGGREGATIONS

````text
GET /my-index-000001/_search
{
  "size": 0,
  "aggs": { --> You could specify multiple aggregations in the same request
    "my-first-agg-name": { --> by different aggregation names
      "terms": {
        "field": "my-field"
      }
    },
    "my-second-agg-name": { --> by different aggregation names
      "avg": {
        "field": "my-other-field"
      }
    }
  }
}
````

## AGGREGATION CACHES

For faster responses, Elasticsearch 
caches the results of frequently run 
aggregations in the shard request 
cache. To get cached results, use 
the same preference string for each 
search. 
If you don’t need search hits, set 
size to 0 in order to avoid filling the 
cache.


````text
GET /my-index-000001/_search?preference=session_id
{
  "size": 0,
  "aggs": {
    "my-first-agg-name": {
      "terms": {
        "field": "my-field"
      }
    }
  }
}
````

## BUCKET AGGREGATIONS

Bucket aggregations create buckets of documents. Each bucket is associated with a 
criterion which determines whether a document in the current context “falls” into it. In 
other words, the buckets effectively define document sets. In addition to the buckets 
themselves, the bucket aggregations also compute and return the number of 
documents that "fell into" each bucket.

There are different bucket aggregators, each with a different "bucketing" 
strategy. Some define a single bucket, some define fixed number of multiple buckets, 
and others dynamically create the buckets during the aggregation process.


## FILTER BUCKET AGGREGATIONS

A single bucket aggregation that narrows the set of documents to those that match a query.

````text
POST /sales/_search?size=0&filter_path=aggregations
{
  "aggs": {
    "avg_price": { "avg": { "field": "price" } },
    "t_shirts": {
      "filter": { "term": { "type": "t-shirt" } },
      "aggs": {
        "avg_price": { "avg": { "field": "price" } }
      }
    }
  }
}
````

````json
{
  "aggregations": {
    "avg_price": { "value": 140.71428571428572 },
    "t_shirts": {
      "doc_count": 3,
      "avg_price": { "value": 128.33333333333334 }
    }
  }
}
````

## DATE RANGE BUCKET AGGREGATIONS

````text
POST /sales/_search?size=0
{
  "aggs": {
    "range": {
      "date_range": {
        "field": "date",
        "format": "MM-yyyy",
        "ranges": [
          { "to": "now-10M/M" }, --> now minus 10 months, rounded down to the start of the month
          { "from": "now-10M/M" } --> >= now minus 10 months, rounded down to the start of the month
        ]
      }
    }
  }
}
````

## METRICS AGGREGATIONS

The aggregations in this family compute metrics based on values extracted in one 
way or another from the documents that are being aggregated. The values are typically 
extracted from the fields of the document (using the field data), but can also be 
generated using scripts.

Numeric metrics aggregations are a special type of metrics aggregation which 
output numeric values. Some aggregations output a single numeric metric (e.g. avg) and 
are called single-value numeric metrics aggregation, others generate multiple metrics 
(e.g. stats) and are called multi-value numeric metrics aggregation.

The distinction between single-value and multi-value numeric metrics aggregations plays a role when 
these aggregations serve as direct sub-aggregations of some bucket aggregations (some 
bucket aggregations enable you to sort the returned buckets based on the numeric 
metrics in each bucket)

## AVG METRIC AGGREGATIONS

A single-value metrics aggregation that computes the average of numeric values that are extracted 
from the aggregated documents. These values can be extracted either from specific numeric fields in the 
documents.

````text
POST /exams/_search?size=0
{
  "aggs": {
    "avg_grade": {
      "avg": {
        "field": "grade" }
    }
  }
}
````

````json
{
  "aggregations": {
    "avg_grade": {
      "value": 75.0
    }
  }
}
````

## SCRIPT METRIC AGGREGATIONS

Let’s say the exam was exceedingly difficult, and you need to apply a grade correction. 
Average a runtime field to get a corrected average:

````text
POST /exams/_search?size=0
{
  "runtime_mappings": {
    "grade.corrected": {
      "type": "double",
      "script": {
        "source": "emit(Math.min(100, doc['grade'].value * params.correction))",
        "params": {
          "correction": 1.2
        }
      }
    }
  },
  "aggs": {
    "avg_corrected_grade": {
      "avg": {
        "field": "grade.corrected"
      }
    }
  }
}
````

## SUM METRIC AGGREGATIONS

A single-value metrics aggregation that sums up numeric values that are extracted from the 
aggregated documents. These values can be extracted either from specific numeric or histogram fields.

````text
POST /sales/_search?size=0
{ 
  "query": {
    "constant_score": {
      "filter": {
        "match": { "type": "hat" }
      }
    }
  },
  "aggs": {
    "hat_prices": { "sum": { "field": "price" } }
  }
}
````

````json
{
  "aggregations": {
    "hat_prices": {
      "value": 450.0
    }
  }
}
````

## SCRIPT METRIC AGGREGATIONS

If you need to get the sum for something more complex than a 
single field, run the aggregation on a runtime field.

````text
POST /exams/_search?size=0
{
  "runtime_mappings": {
    "price.weighted": {
      "type": "double",
      "script": "double price = doc['price'].value; if (doc['promoted'].value) { price *= 0.8; } emit(price); "
    }
  },
  "query": {
    "constant_score": {
      "filter": {
        "match": { "type": "hat" }
      }
    }
  },
  "aggs": {
    "hat_prices": {
      "sum": {
        "field": "price.weighted"
      }
    }
  }
}
````

## PIPELINE AGGREGATIONS

Pipeline aggregations work on the outputs produced from other aggregations rather than from 
document sets, adding information to the output tree. There are many different types of pipeline 
aggregation, each computing different information from other aggregations, but these types can 
be broken down into two families:

- Parent
A family of pipeline aggregations that is provided with the output of its parent aggregation 
and can compute new buckets or new aggregations to add to existing buckets.
- Sibling
Pipeline aggregations that are provided with the output of a sibling aggregation and can 
compute a new aggregation which will be at the same level as the sibling aggregation.
- 
https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-pipeline.html