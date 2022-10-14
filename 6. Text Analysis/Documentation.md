## Analyzer
- Only text fields support the analyzer mapping parameter.
- Testing analyzers before using them in production
- The analyzer setting can not be updated on existing fields using the update mapping API

````text
When the built-in analyzers do not fulfill your needs, 
you can create a custom analyzer which uses the appropriate combination of:

- zero or more character filters
- a tokenizer
- zero or more token filters.
````

- Standard Analyzer
````text
The standard analyzer divides text into terms on word boundaries, as defined by the Unicode Text Segmentation algorithm.
It removes most punctuation, lowercases terms, and supports removing stop words.
````

- Simple Analyzer
````text
The simple analyzer divides text into terms whenever it encounters a character which is not a letter. It lowercases all terms.
````
- Whitespace Analyzer
````text
The whitespace analyzer divides text into terms whenever it encounters any whitespace character. It does not lowercase terms.
````
- Stop Analyzer
````text
The stop analyzer is like the simple analyzer, but also supports removal of stop words.
````
- Keyword Analyzer
````text
The keyword analyzer is a “noop” analyzer that accepts whatever text it is given and outputs the exact same text as a single term.
````
- Pattern Analyzer
````text
The pattern analyzer uses a regular expression to split the text into terms. It supports lower-casing and stop words.
````

- Language Analyzers
````text
Elasticsearch provides many language-specific analyzers like english or french.
````

- Fingerprint Analyzer
````text
The fingerprint analyzer is a specialist analyzer which creates a fingerprint which can be used for duplicate detection.
````

- Custom analyzers
````text
If you do not find an analyzer suitable for your needs,
you can create a custom analyzer which combines the appropriate character filters, 
tokenizer, and token filters.
````

## Built-in Analyzer example

````text
PUT my-index-000001
{
  "mappings": {
    "properties": {
      "title": {
        "type": "text",
        "analyzer": "whitespace"
      }
    }
  }
}
````

## Custom Analyzer example

````text
PUT my-index-000001
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_custom_analyzer": {    <-- name of custom analyzer
          "type": "custom",        <-- type of analyzer
          "tokenizer": "standard", <-- type of tokenizer
          "char_filter": [         <-- list of char filters
            "html_strip"
          ],
          "filter": [              <-- list of filters
            "lowercase",
            "asciifolding"
          ]
        }
      }
    }
  }
}
````

## Test custom analyzer
````text
POST my-index-000001/_analyze
````
````json
{
  "analyzer": "my_custom_analyzer",
  "text": "Is this <b>déjà vu</b>?"
}
````



## Normalizer
- The normalizer property of keyword fields is similar to analyzer except that it guarantees that the analysis chain produces a single token.