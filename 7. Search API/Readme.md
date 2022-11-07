# QUERY DSL

## DSL - Domain Specific Language
### There are 2 types of clauses:
- Leaf query clauses
````text
Leaf query clauses look for a particular value in a particular field, such as the match, 
term, range or other similar queries. These queries can be used by themselves.
````

- Compound query clauses
````text
Compound query clauses wrap other leaf or compound queries and are used to combine 
multiple querie
````

### SCORE AND RELEVANCE:
By default, Elasticsearch sorts matching search results by relevance score, which measures 
how well each document matches a query.
The relevance score is a positive floating point number, returned in the _score metadata field of 
the search API. The higher the _score, the more relevant the document is.

While each query type can calculate relevance scores differently, score calculation also depends on whether 
the query clause is run in a query or filter context.

## QUERY AND FILTER CONTEXT:
- Query context:
````text
In the query context, a query clause answers the question
“How well does this document match this query clause?”
Besides deciding whether or not the document matches, 
the query clause also calculates a relevance score in 
the _score metadata field.
````

- Filter context:
````text
In a filter context, a query clause answers the question
“Does this document match this query clause?”
The answer is a simple Yes or No scores are calculated.
Frequently used filters will be cached automatically by Elasticsearch, to speed up performance.
It is good to filter first, then to calculate score
````

## FULL TEXT QUERIES OVERVIEW
- A set of queries designed to work on analyzed text (so at least tokenized)
- While the target of the previous queries was to match a single term these can go beyond
- To get some intuition about them think „Google”, while they are no way near as advanced, they 
can be used to build a fully functional site search

## MATCH QUERY
Returns documents that match a provided text, 
number, date or boolean value. The provided text is 
analyzed before matching.
The match query is the standard query for 
performing a full-text search, including options for 
fuzzy matching.

````json
{
  "query": {
    "match": {
      "title": {
        "query": "sound of thunder"
      }
    }
  }
}
````

## MATCH QUERY - BOOLEAN SUBTYPE
- Has other variants for different type of matches
- Basically, it is a more concise way of creating a bool query
The example matches:
- „A Sound of Thunder”
- „Delicate Sound of Thunder”

````json
{
  "query": {
    "match": {
      "title": {
        "query": "sound of thunder",
        "operator": "and"
      }
    }
  }
}

````

## MATCH QUERY - BOOLEAN SUBTYPE, RELAXED MATCHING
- A way to define a relaxed requirements on number of terms matched
- In the following examples the minimum should match expression defines our match relaxation. 
While these are simple expressions, they can be composed depending on the input length to form a 
more complex definition that is more universal and practical
- For these settings – we define a 3-term match, but we only require two of them for document to 
appear on the result list

````json
{
  "query": {
    "match": {
      "name": {
        "query": "sound of thunder",
        "minimum_should_match": 2
      }
    }
  }
}
````
````json
{
  "query": {
    "match": {
      "name": {
        "query": "sound of thunder",
        "minimum_should_match": "67%"
      }
    }
  }
}
````

## MATCH PHRASE QUERY
The match_phrase query analyzes the text 
and creates a phrase query out of the 
analyzed text.

````json
{
  "query": {
    "match_phrase": {
      "query": "this is a test"
    }
  }
}

````

## QUERY STRING QUERY
- Can be something you bind to the search 
box itself (the one for the benefits to use 
this feature)
- For the more generic search box you might 
use Simple Query String Query. This one 
does not throw any exceptions – it just 
removes the invalid parts
- The provided query is parsed from text —
then internally the combination of multiple 
queries is created and executed

````json
{
  "query": {
    "query_string": {
      "default_field": "name",
      "query": "deep purple"
    }
  }
}
````

````json
{
  "query": {
    "query_string": {
      "default_field": "name",
      "query": "deep purple productSubclass:\"MUSIC DVD\""
    }
  }
}
````

Your application can realize that user is in the video section of the store and glue this in.
This is a phrase that should be matched to the property „productSubclass”

````json
{
  "query": {
    "query_string": {
      "default_field": "name",
      "query": "(deep purple productSubclass:\"MUSIC DVD\") AND freeShipping:true"
    }
  }
}
````

Hmm, somebody wants free shipping for whatever we found?
The parentheses do a bit of grouping, the default operator if not set otherwise is OR, to keep 
things neat and clean the parantheses were added

## GEO QUERIES

Elasticsearch supports two types of geo data: geo_point fields which support lat/lon pairs, and geo_shape fields, 
which support points, lines, circles, polygons, multi-polygons, etc.


````text
PUT my-index-000001
{
  "mappings": {
    "properties": {
      "location": {
        "type": "geo_point"
      }
    }
  }
}
````

````text
PUT my-index-000001/_doc/1
{
  "text": "Geopoint as an object",
  "location": {
    "lat": 41.12,
    "lon": -71.34
  }
}
````

## MLT

#### More Like This query
The More Like This Query finds documents that are "like" 
a given document or set of documents. In order to do so, 
MLT selects a set of representative terms of these input 
documents, forms a query using these terms, executes 
the query and returns the results. The user controls the 
input documents, how the terms should be selected and 
how the query is formed.

The simplest use case consists of asking for documents 
that are similar to a provided piece of text. Here, we are 
asking for all movies that have some text similar to "Once 
upon a time" in their "title" and in their "description" fields, 
limiting the number of selected terms to 12.

````text
GET /_search
{
  "query": {
    "more_like_this": {
      "fields": [
        "title",
        "description"
      ],
      "like": "Once upon a time",
      "min_term_freq": 1,
      "max_query_terms": 12
    }
  }
}
````

## SCRIPT QUERY

- Filters documents based on a provided script.
- The script query is typically used in a filter context.
- Using scripts can reult in slower search speeds.

````text
GET /_search
{
  "query": {
    "bool": {
      "filter": {
        "script": {
          "script": """
          double amount = doc['amount'].value;
if (doc['type'].value == 'expense') {
amount *= -1;
}
return amount < 10;
"""
}
}}}}
````

## SCRIPT SCORE QUERY

We could use script to provide custom score for returned documents.
The following script_score query assigns each returned document a score equal to 
the my-int field value divided by 10.

````text
GET /_search
{
  "query": {
    "script_score": {
      "query": {
        "match": { "message": "elasticsearch" }
      },
      "script": {
        "source": "doc['my-int'].value / 10 "
      }
    }
  }
}
````

## FUZZY

Returns documents that contain terms 
similar to the search term, as measured by 
a Levenshtein edit distance

An edit distance is the number of one character changes needed to turn one term into another.

These changes can include: 
- Changing a character (box → fox) 
- Removing a character (black → lack)
- Inserting a character (sic → sick) 
- Transposing two adjacent characters (act → cat)

````text
GET /_search 
{
  "query": {
    "fuzzy": {
      "user.id": {
        "value": "ki"
      }
    }
  }
}
````

## PERCOLATE

The percolate query can be used to match queries stored in an index. 
The percolate query itself contains the document that will be used as query to match with the stored queries.

https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-percolate-query.html

RANK FEATURE QUERY:
We could boost the relevance score of documents based on the numeric value of a rank_feature or rank_features field.

https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-rank-feature-query.htm