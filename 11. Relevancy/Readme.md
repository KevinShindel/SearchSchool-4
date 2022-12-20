# Relevancy in ELK

### Elastic uses scoring algorithm that evaluate each matched document with some relevancy 
measurement. The bigger is this number, the higher results (document) will be in hits
Approximate scoring formula which is good for first level of understanding is following:
score(q,d) = queryNorm(q) * coord(q,d) * ∑ (tf(t in d) * idf(t)² * t.getBoost() * norm(t,d)) (t in q)
https://www.elastic.co/guide/en/elasticsearch/guide/current/practical-scoring-function.html
The terms of this function mean the following:
score (q,d): a relevance score of document d for query q
queryNorm (q): query normalization factor
coord (q,d): query coordination factor
tf (t in d): term frequency of term t in document d
idf (t): inverse document frequency for term t 
t.getBoost(): the boost applied to the query 
norm(t,d) – the field-length norm

### Scoring components
Term Frequency (TF) is quite a simple concept to start with. It simply calculates the number of times 
a given “term” / “word” appears in the document. It assumes that the document that has 5 matches 
of the query term is more relevant than a document with just a single appearance of this term.
The TF is calculated using the following formula:
tf(t in d) = √frequency
Inverse document frequency (IDF) assigns low weight/relevance to terms that appear frequently in 
all of the documents in the index. For example, the terms “and” and “in” have low relevance because 
normally they are not unique to any document of the index.
IDF is calculated using the following formula:
idf = 1 + ln(numDocs/(docFreq + 1))

In the case of a multi-term query, the coordination factor rewards the documents that contain a 
higher number of terms of that query. The more query terms appear in the document the more 
relevance it might have.
The coordination factor uses the following formula:
term score * number of matching terms / total number of terms in the query. 
Query Normalization Factor is the ratio that aims to make results of different queries comparable. It 
is calculated at the beginning of each query using the following formula:
queryNorm = 1 / √sumOfSquaredWeights, where the sumOfSquaredWeights is computed by adding 
together the IDF of each term in the query, squared

Field length normalization (norm) is the inverse square root of the number of terms in the field:
norm = 1/sqrt(numFieldTerms)
The value of this parameter depends on the document field length in which a match with the query 
was found. The smaller length of the field the greater the value of the parameter. It makes sense if 
you think that the reference to the terms of the request in the field “title” is more important than in the 
“description.
Boost is a coefficient that could be assigned to the query in order to multiply the score before 
returning. Only values > 0 are supported. In order to give positive boost – assign value > 1, and for 
negative boost – assign value < 1. Boosting is powerful technique to manipulate scores via simple 
rules or conditions

### Similarity module in Elasticsearch
Elastic is bundled with different types of similarities (different formulas and concepts). Similarity could be 
configured per field, meaning that via the mapping one can define a different similarity per field.
Available similarities:
- BM25 – default similarity based on TF-IDF, supposed to work better on short fields
- DFR – implements divergence from randomness. For more information -
https://lucene.apache.org/core/9_1_0/core/org/apache/lucene/search/similarities/DFRSimilarity.html
- DFI – implements divergence from independence. For more information -
https://trec.nist.gov/pubs/trec21/papers/irra.web.nb.pdf
- IB – similarity based on the concept that the information content in any symbolic distribution sequence is 
primarily determined by the repetitive usage of its basic elements. For written texts this challenge would 
correspond to comparing the writing styles of different authors. For more information -
https://lucene.apache.org/core/9_1_0/core/org/apache/lucene/search/similarities/IBSimilarity.html
- For other types of similarities https://www.elastic.co/guide/en/elasticsearch/reference/current/indexmodules-similarity.html

### Relevancy metrics
In order to access search system or particular query one would need to have some metrics that 
would help compare and rate the “quality” or relevancy of the search
There are online and offline metrics. 
Online metrics are usually extracted out of search (or similar behavioural) logs. Those metrics are 
often used in A/B testing scenarios. Examples of those metrics could be:
- Session abandonment rate (which is rate of search sessions which didn’t end up with at least one 
click on the product)
- Session success rate (which is rate of search sessions that end up with success. There are 
multiply ways to define “success” and it could be done with business. Examples could be –
clicking on the product, adding it to basket, or time user spends “looking” at the product)
- Zero results queries (which is rate of queries ended up without any results, often this is 
considered to be worst user experience in e-commerce)

Offline metrics are rather created based on judgements dataset, where experts provides the score for 
the documents for specified query. Those scores could be binary (relevant or not) or some number 
representation (for example from 0 to 10, where 0 means non-relevant completely and 10 means the 
most relevant result)
Offline metrics are:
- Precision
- Recall
- Precision at K
- Mean Average Precision
- NDCG
- F-score
- Etc…
Let’s take a deeper look at some of them

### Precision and recall

Precision is the fraction of relevant instances among the retrieved 
instances, while is the fraction of relevant instances that were retrieved. 
Both precision and recall are therefore based on relevance.
A perfect precision score of 1.0 means that every result retrieved by a 
search was relevant (but says nothing about whether all relevant 
documents were retrieved) whereas a perfect recall score of 1.0 
means that all relevant documents were retrieved by the search (but 
says nothing about how many irrelevant documents were also 
retrieved).
Precision at k – corresponds to number of relevant results out of first k
ones. This is usually considered better metrics in web-scale search 
engines when each query might have thousands of relevant results

### Combined relevancy metrics
Sometimes it’s tricky to balance several metrics like precision and recall, especially in the optimization 
task, hence there are several combined ones:
• F-score – which is weighted harmonic mean of precision and recall, which equally weighted precision 
and recall the formula will be the following
F1 = (2 * precision * recall) / (precision + recall)
• Discounted cumulative gain - uses a graded relevance scale of documents from the result set to 
evaluate the usefulness, or gain, of a document based on its position in the result list. The premise of 
DCG is that highly relevant documents appearing lower in a search result list should be penalized as 
the graded relevance value is reduced logarithmically proportional to the position of the result.
DCG at P = sum (i = 1 to P) (relevance(i) / log(i + 1), 
https://en.wikipedia.org/wiki/F-score
https://en.wikipedia.org/wiki/Discounted_cumulative_gain


### How to troubleshoot and check scoring
In order to understand how the following score was calculated, Elasticsearch offers Explain API
https://www.elastic.co/guide/en/elasticsearch/reference/current/search-explain.html
This request checks how the score will be calculated for 
document with id 0 and the following match query

GET /my-index-000001/_explain/0
````json
{ 
  "query" : { 
    "match" : { 
      "message" : "elasticsearch"
    } 
  } 
}
````

### Simple ways to control relevancy – Boosting query
Returns documents matching a positive query while reducing the relevance score of documents that also 
match a negative query.
You can use the boosting query to demote certain documents without excluding them from the search 
results
GET /_search 
````json
{ 
  "query": { 
    "boosting": { 
      "positive": { 
        "term": { "text": "apple" } }, 
      "negative": { "term": { "text": "pie tart fruit crumble tree" } }, 
      "negative_boost": 0.5 
    } 
  } 
}
````

https://www.elastic.co/blog/how-to-improve-elasticsearch-search-relevance-with-boolean-queries
https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-boosting-query.html

### Simple ways to control relevancy – Constant score
Often, it’s important to match several boolean clauses and rank them accordingly to the number of 
matches, not to sum or individual score. In this constant score could be used. It wraps a filter query and 
returns every matching document with a relevance score equal to the boost parameter value.
GET /_search 
````json
{ 
  "query": { 
    "constant_score": { 
      "filter": { 
        "term": { "user.id": "kimchy" } }, 
      "boost": 1.2 
    } 
  } 
}
````
https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-constant-score-query.htm

### Simple ways to control relevancy – Disjunction max query
Returns documents matching one or more wrapped queries, called query clauses or clauses.
If a returned document matches multiple query clauses, the dis_max query assigns the document the 
highest relevance score from any matching clause, plus a tie breaking increment for any additional 
matching subqueries.
GET /_search 
````json
{ 
  "query": { 
    "dis_max": { 
      "queries": [ 
        { "term": { "title": "Quick pets" } }, 
        { "term": { "body": "Quick pets" } } 
      ], 
      "tie_breaker": 0.7 
    } 
  } 
}
````

https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-dis-max-query.html

### Simple ways to control relevancy – Function score 
The function_score allows you to modify the score of documents that are retrieved by a query. To use 
function_score, the user has to define a query and one or more functions, that compute a new score for 
each document returned by the query.
The function_score query provides several types of score functions.
• script_score
• weight
• random_score
• field_value_factor
• decay functions: gauss, linear, exp
For more details, please check function score documentation
https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-function-score-query.htm