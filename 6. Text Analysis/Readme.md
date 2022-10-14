## BUILT-IN ANALYZERS

Elasticsearch ships with a wide range of built-in analyzers, which can be used in any index without further
configuration

#### Standard  Analyzer

The standard analyzer divides text into terms on word boundaries, as defined by the Unicode Text Segmentation algorithm.
It removes most punctuation, lowercases terms, and supports removing stop words.

````text
POST _analyze
````

````json
 {
  "tokenizer": "standard",
  "filter": [
    "lowercase",
    "asciifolding"
  ],
  "text": "Is this déja vu?"
}
````

````json
{
  "tokens": [
    {
      "token": "is",
      "start_offset": 0,
      "end_offset": 2,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "this",
      "start_offset": 3,
      "end_offset": 7,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "deja",
      "start_offset": 8,
      "end_offset": 12,
      "type": "<ALPHANUM>",
      "position": 2
    },
    {
      "token": "vu",
      "start_offset": 13,
      "end_offset": 15,
      "type": "<ALPHANUM>",
      "position": 3
    }
  ]
}
````

#### Whitespace  Analyzer

The whitespace analyzer divides text into terms whenever it encounters any whitespace character. It does not lowercase
terms.Keyword Analyzer

````text
POST _analyze
````

````json
{
  "analyzer": "whitespace",
  "text": "The quick brown fox."
}
````

````json
{
  "tokens": [
    {
      "token": "The",
      "start_offset": 0,
      "end_offset": 3,
      "type": "word",
      "position": 0
    },
    {
      "token": "quick",
      "start_offset": 4,
      "end_offset": 9,
      "type": "word",
      "position": 1
    },
    {
      "token": "brown",
      "start_offset": 10,
      "end_offset": 15,
      "type": "word",
      "position": 2
    },
    {
      "token": "fox.",
      "start_offset": 16,
      "end_offset": 20,
      "type": "word",
      "position": 3
    }
  ]
}
````

#### The keyword analyzer

is a “noop” analyzer that accepts whatever text it is given and outputs the exact same text as a single term.

## TOKENIZERS

A tokenizer receives a stream of characters, breaks it up into individual tokens (usually individual words), and outputs
a stream of tokens. For instance, a whitespace tokenizer breaks text into tokens whenever it sees any whitespace. It
would convert the text  "Quick brown fox!" into the terms  [Quick, brown, fox!].

#### Standard Tokenizer
The standard tokenizer divides text into terms on word boundaries, as defined by the Unicode Text Segmentation algorithm. It removes most punctuation symbols. It is the best choice for most languages.
````json
{
  "tokenizer": "standard",
  "text": " The 2 QUICK Brown-Foxes jumped over the lazy  dog's bone. "
}
````
````json
{
  "tokens": [
    {
      "token": "The",
      "start_offset": 1,
      "end_offset": 4,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "2",
      "start_offset": 5,
      "end_offset": 6,
      "type": "<NUM>",
      "position": 1
    },
    {
      "token": "QUICK",
      "start_offset": 7,
      "end_offset": 12,
      "type": "<ALPHANUM>",
      "position": 2
    },
    {
      "token": "Brown",
      "start_offset": 13,
      "end_offset": 18,
      "type": "<ALPHANUM>",
      "position": 3
    },
    {
      "token": "Foxes",
      "start_offset": 19,
      "end_offset": 24,
      "type": "<ALPHANUM>",
      "position": 4
    },
    {
      "token": "jumped",
      "start_offset": 25,
      "end_offset": 31,
      "type": "<ALPHANUM>",
      "position": 5
    },
    {
      "token": "over",
      "start_offset": 32,
      "end_offset": 36,
      "type": "<ALPHANUM>",
      "position": 6
    },
    {
      "token": "the",
      "start_offset": 37,
      "end_offset": 40,
      "type": "<ALPHANUM>",
      "position": 7
    },
    {
      "token": "lazy",
      "start_offset": 41,
      "end_offset": 45,
      "type": "<ALPHANUM>",
      "position": 8
    },
    {
      "token": "dog's",
      "start_offset": 47,
      "end_offset": 52,
      "type": "<ALPHANUM>",
      "position": 9
    },
    {
      "token": "bone",
      "start_offset": 53,
      "end_offset": 57,
      "type": "<ALPHANUM>",
      "position": 10
    }
  ]
}
````

#### Letter Tokenizer
The letter tokenizer divides text into terms whenever it encounters a character which is not a letter.
````json
{
  "tokenizer": "letter",
  "text": " The 2 QUICK Brown-Foxes jumped over the lazy  dog's bone. "
}
````
````json
{
  "tokens": [
    {
      "token": "The",
      "start_offset": 1,
      "end_offset": 4,
      "type": "word",
      "position": 0
    },
    {
      "token": "QUICK",
      "start_offset": 7,
      "end_offset": 12,
      "type": "word",
      "position": 1
    },
    {
      "token": "Brown",
      "start_offset": 13,
      "end_offset": 18,
      "type": "word",
      "position": 2
    },
    {
      "token": "Foxes",
      "start_offset": 19,
      "end_offset": 24,
      "type": "word",
      "position": 3
    },
    {
      "token": "jumped",
      "start_offset": 25,
      "end_offset": 31,
      "type": "word",
      "position": 4
    },
    {
      "token": "over",
      "start_offset": 32,
      "end_offset": 36,
      "type": "word",
      "position": 5
    },
    {
      "token": "the",
      "start_offset": 37,
      "end_offset": 40,
      "type": "word",
      "position": 6
    },
    {
      "token": "lazy",
      "start_offset": 41,
      "end_offset": 45,
      "type": "word",
      "position": 7
    },
    {
      "token": "dog",
      "start_offset": 47,
      "end_offset": 50,
      "type": "word",
      "position": 8
    },
    {
      "token": "s",
      "start_offset": 51,
      "end_offset": 52,
      "type": "word",
      "position": 9
    },
    {
      "token": "bone",
      "start_offset": 53,
      "end_offset": 57,
      "type": "word",
      "position": 10
    }
  ]
}
````

#### Lowercase Tokenizer
The lowercase tokenizer, like the letter tokenizer, divides text into terms whenever it encounters a character which is not a letter, but it also lowercases all terms.

````json
{
  "tokenizer": "lowercase",
  "text": " The 2 QUICK Brown-Foxes jumped over the lazy  dog's bone. "
}
````
````json
{
  "tokens": [
    {
      "token": "the",
      "start_offset": 1,
      "end_offset": 4,
      "type": "word",
      "position": 0
    },
    {
      "token": "quick",
      "start_offset": 7,
      "end_offset": 12,
      "type": "word",
      "position": 1
    },
    {
      "token": "brown",
      "start_offset": 13,
      "end_offset": 18,
      "type": "word",
      "position": 2
    },
    {
      "token": "foxes",
      "start_offset": 19,
      "end_offset": 24,
      "type": "word",
      "position": 3
    },
    {
      "token": "jumped",
      "start_offset": 25,
      "end_offset": 31,
      "type": "word",
      "position": 4
    },
    {
      "token": "over",
      "start_offset": 32,
      "end_offset": 36,
      "type": "word",
      "position": 5
    },
    {
      "token": "the",
      "start_offset": 37,
      "end_offset": 40,
      "type": "word",
      "position": 6
    },
    {
      "token": "lazy",
      "start_offset": 41,
      "end_offset": 45,
      "type": "word",
      "position": 7
    },
    {
      "token": "dog",
      "start_offset": 47,
      "end_offset": 50,
      "type": "word",
      "position": 8
    },
    {
      "token": "s",
      "start_offset": 51,
      "end_offset": 52,
      "type": "word",
      "position": 9
    },
    {
      "token": "bone",
      "start_offset": 53,
      "end_offset": 57,
      "type": "word",
      "position": 10
    }
  ]
}
````

#### Whitespace Tokenizer
The whitespace tokenizer divides text into terms whenever it encounters any whitespace character.
````json
{
  "tokenizer": "whitespace",
  "text": " The 2 QUICK Brown-Foxes jumped over the lazy  dog's bone. "
}
````
````json
{
  "tokens": [
    {
      "token": "The",
      "start_offset": 1,
      "end_offset": 4,
      "type": "word",
      "position": 0
    },
    {
      "token": "2",
      "start_offset": 5,
      "end_offset": 6,
      "type": "word",
      "position": 1
    },
    {
      "token": "QUICK",
      "start_offset": 7,
      "end_offset": 12,
      "type": "word",
      "position": 2
    },
    {
      "token": "Brown-Foxes",
      "start_offset": 13,
      "end_offset": 24,
      "type": "word",
      "position": 3
    },
    {
      "token": "jumped",
      "start_offset": 25,
      "end_offset": 31,
      "type": "word",
      "position": 4
    },
    {
      "token": "over",
      "start_offset": 32,
      "end_offset": 36,
      "type": "word",
      "position": 5
    },
    {
      "token": "the",
      "start_offset": 37,
      "end_offset": 40,
      "type": "word",
      "position": 6
    },
    {
      "token": "lazy",
      "start_offset": 41,
      "end_offset": 45,
      "type": "word",
      "position": 7
    },
    {
      "token": "dog's",
      "start_offset": 47,
      "end_offset": 52,
      "type": "word",
      "position": 8
    },
    {
      "token": "bone.",
      "start_offset": 53,
      "end_offset": 58,
      "type": "word",
      "position": 9
    }
  ]
}
````

#### UAX URL Email Tokenizer
The uax_url_email tokenizer is like the standard tokenizer except that it recognises URLs and email addresses as single tokens.
````json
{
  "tokenizer": "uax_url_email",
  "text": " The 2 QUICK Brown-Foxes jumped over the lazy  dog's bone. kevin@yahoo.com. Visit our site https://airgun.org.ua/forum"
}
````
````json
{
  "tokens": [
    {
      "token": "The",
      "start_offset": 1,
      "end_offset": 4,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "2",
      "start_offset": 5,
      "end_offset": 6,
      "type": "<NUM>",
      "position": 1
    },
    {
      "token": "QUICK",
      "start_offset": 7,
      "end_offset": 12,
      "type": "<ALPHANUM>",
      "position": 2
    },
    {
      "token": "Brown",
      "start_offset": 13,
      "end_offset": 18,
      "type": "<ALPHANUM>",
      "position": 3
    },
    {
      "token": "Foxes",
      "start_offset": 19,
      "end_offset": 24,
      "type": "<ALPHANUM>",
      "position": 4
    },
    {
      "token": "jumped",
      "start_offset": 25,
      "end_offset": 31,
      "type": "<ALPHANUM>",
      "position": 5
    },
    {
      "token": "over",
      "start_offset": 32,
      "end_offset": 36,
      "type": "<ALPHANUM>",
      "position": 6
    },
    {
      "token": "the",
      "start_offset": 37,
      "end_offset": 40,
      "type": "<ALPHANUM>",
      "position": 7
    },
    {
      "token": "lazy",
      "start_offset": 41,
      "end_offset": 45,
      "type": "<ALPHANUM>",
      "position": 8
    },
    {
      "token": "dog's",
      "start_offset": 47,
      "end_offset": 52,
      "type": "<ALPHANUM>",
      "position": 9
    },
    {
      "token": "bone",
      "start_offset": 53,
      "end_offset": 57,
      "type": "<ALPHANUM>",
      "position": 10
    },
    {
      "token": "kevin@yahoo.com.",
      "start_offset": 59,
      "end_offset": 75,
      "type": "<EMAIL>",
      "position": 11
    },
    {
      "token": "Visit",
      "start_offset": 76,
      "end_offset": 81,
      "type": "<ALPHANUM>",
      "position": 12
    },
    {
      "token": "our",
      "start_offset": 82,
      "end_offset": 85,
      "type": "<ALPHANUM>",
      "position": 13
    },
    {
      "token": "site",
      "start_offset": 86,
      "end_offset": 90,
      "type": "<ALPHANUM>",
      "position": 14
    },
    {
      "token": "https://airgun.org.ua/forum",
      "start_offset": 91,
      "end_offset": 118,
      "type": "<URL>",
      "position": 15
    }
  ]
}
````

#### Classic Tokenizer
The classic tokenizer is a grammar based tokenizer for the English Language.
````json
{
  "tokenizer": "classic",
  "text": " The 2 QUICK Brown-Foxes jumped over the lazy  dog's bone. "
}
````
````json
{
  "tokens": [
    {
      "token": "The",
      "start_offset": 1,
      "end_offset": 4,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "2",
      "start_offset": 5,
      "end_offset": 6,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "QUICK",
      "start_offset": 7,
      "end_offset": 12,
      "type": "<ALPHANUM>",
      "position": 2
    },
    {
      "token": "Brown",
      "start_offset": 13,
      "end_offset": 18,
      "type": "<ALPHANUM>",
      "position": 3
    },
    {
      "token": "Foxes",
      "start_offset": 19,
      "end_offset": 24,
      "type": "<ALPHANUM>",
      "position": 4
    },
    {
      "token": "jumped",
      "start_offset": 25,
      "end_offset": 31,
      "type": "<ALPHANUM>",
      "position": 5
    },
    {
      "token": "over",
      "start_offset": 32,
      "end_offset": 36,
      "type": "<ALPHANUM>",
      "position": 6
    },
    {
      "token": "the",
      "start_offset": 37,
      "end_offset": 40,
      "type": "<ALPHANUM>",
      "position": 7
    },
    {
      "token": "lazy",
      "start_offset": 41,
      "end_offset": 45,
      "type": "<ALPHANUM>",
      "position": 8
    },
    {
      "token": "dog's",
      "start_offset": 47,
      "end_offset": 52,
      "type": "<APOSTROPHE>",
      "position": 9
    },
    {
      "token": "bone",
      "start_offset": 53,
      "end_offset": 57,
      "type": "<ALPHANUM>",
      "position": 10
    }
  ]
}
````

#### Thai Tokenizer
The thai tokenizer segments Thai text into words.
````json
{
  "tokenizer": "thai",
  "text": "การที่ได้"
}
````
````json
{
  "tokens": [
    {
      "token": "การ",
      "start_offset": 0,
      "end_offset": 3,
      "type": "word",
      "position": 0
    },
    {
      "token": "ที่",
      "start_offset": 3,
      "end_offset": 6,
      "type": "word",
      "position": 1
    },
    {
      "token": "ได้",
      "start_offset": 6,
      "end_offset": 9,
      "type": "word",
      "position": 2
    }
  ]
}
````

````json
{
  "tokens": [
    {
      "token": "The",
      "start_offset": 1,
      "end_offset": 4,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "2",
      "start_offset": 5,
      "end_offset": 6,
      "type": "<NUM>",
      "position": 1
    },
    {
      "token": "QUICK",
      "start_offset": 7,
      "end_offset": 12,
      "type": "<ALPHANUM>",
      "position": 2
    },
    {
      "token": "Brown",
      "start_offset": 13,
      "end_offset": 18,
      "type": "<ALPHANUM>",
      "position": 3
    },
    {
      "token": "Foxes",
      "start_offset": 19,
      "end_offset": 24,
      "type": "<ALPHANUM>",
      "position": 4
    },
    {
      "token": "jumped",
      "start_offset": 25,
      "end_offset": 31,
      "type": "<ALPHANUM>",
      "position": 5
    },
    {
      "token": "over",
      "start_offset": 32,
      "end_offset": 36,
      "type": "<ALPHANUM>",
      "position": 6
    },
    {
      "token": "the",
      "start_offset": 37,
      "end_offset": 40,
      "type": "<ALPHANUM>",
      "position": 7
    },
    {
      "token": "lazy",
      "start_offset": 41,
      "end_offset": 45,
      "type": "<ALPHANUM>",
      "position": 8
    },
    {
      "token": "dog's",
      "start_offset": 47,
      "end_offset": 52,
      "type": "<ALPHANUM>",
      "position": 9
    },
    {
      "token": "bone",
      "start_offset": 53,
      "end_offset": 57,
      "type": "<ALPHANUM>",
      "position": 10
    }
  ]
}
````

### Path hierarchy
````text
POST /_analyze
````
````json
 { "tokenizer": "path_hierarchy", "text": "/etc/elasticsearch/logs" }
````
````json
{
  "tokens": [
    {
      "token": "/etc",
      "start_offset": 0,
      "end_offset": 4,
      "type": "word",
      "position": 0
    },
    {
      "token": "/etc/elasticsearch",
      "start_offset": 0,
      "end_offset": 18,
      "type": "word",
      "position": 0
    },
    {
      "token": "/etc/elasticsearch/logs",
      "start_offset": 0,
      "end_offset": 23,
      "type": "word",
      "position": 0
    }
  ]
}
````

## Partial Word Tokenizer
These tokenizers break up text or words into small fragments, for partial word matching:

### N-Gram Tokenizer
The ngram tokenizer can break up text into words when it encounters any of a list of specified characters (e.g. whitespace or punctuation), then it returns n-grams of each word: a sliding window of continuous letters, e.g. quick → [qu, ui, ic, ck].
````json
{
  "tokenizer": "ngram",
  "text": "Fox"
}
````
````json
{
  "tokens": [
    {
      "token": "F",
      "start_offset": 0,
      "end_offset": 1,
      "type": "word",
      "position": 0
    },
    {
      "token": "Fo",
      "start_offset": 0,
      "end_offset": 2,
      "type": "word",
      "position": 1
    },
    {
      "token": "o",
      "start_offset": 1,
      "end_offset": 2,
      "type": "word",
      "position": 2
    },
    {
      "token": "ox",
      "start_offset": 1,
      "end_offset": 3,
      "type": "word",
      "position": 3
    },
    {
      "token": "x",
      "start_offset": 2,
      "end_offset": 3,
      "type": "word",
      "position": 4
    }
  ]
}
````
### Edge N-Gram Tokenizer
The edge_ngram tokenizer can break up text into words when it encounters any of a list of specified characters (e.g. whitespace or punctuation), then it returns n-grams of each word which are anchored to the start of the word, e.g. quick → [q, qu, qui, quic, quick].
````json
{
  "tokenizer": "edge_ngram",
  "text": "Quick Fox"
}
````
````json
{
  "tokens": [
    {
      "token": "Q",
      "start_offset": 0,
      "end_offset": 1,
      "type": "word",
      "position": 0
    },
    {
      "token": "Qu",
      "start_offset": 0,
      "end_offset": 2,
      "type": "word",
      "position": 1
    }
  ]
}
````

#### TOKEN FILTERS

Elasticsearch has set filters that work on the token produced by analyzers




## Structured Text Tokenizer
The following tokenizers are usually used with structured text like identifiers, email addresses, zip codes, and paths, rather than with full text:

### Keyword Tokenizer
The keyword tokenizer is a “noop” tokenizer that accepts whatever text it is given and outputs the exact same text as a single term. It can be combined with token filters like lowercase to normalise the analysed terms.

### Pattern Tokenizer
The pattern tokenizer uses a regular expression to either split text into terms whenever it matches a word separator, or to capture matching text as terms.

### Simple Pattern Tokenizer
The simple_pattern tokenizer uses a regular expression to capture matching text as terms. It uses a restricted subset of regular expression features and is generally faster than the pattern tokenizer.

### Char Group Tokenizer
The char_group tokenizer is configurable through sets of characters to split on, which is usually less expensive than running regular expressions.

### Simple Pattern Split Tokenizer
The simple_pattern_split tokenizer uses the same restricted regular expression subset as the simple_pattern tokenizer, but splits the input at matches rather than returning the matches as terms.

### Path Tokenizer
The path_hierarchy tokenizer takes a hierarchical value like a filesystem path, splits on the path separator, and emits a term for each component in the tree, e.g. /foo/bar/baz → [/foo, /foo/bar, /foo/bar/baz ].



## Create Index with Analyzer
````text
PUT analyzer-index
````
````json
{ 
    "settings": {
        "analysis": {
          "analyzer": {
            "my_analyzer":{
              "type":"custom",
              "tokenizer":"standard",
              "filter":[
                "lowercase"
                ]
            }
          }
        }, 
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
    "mappings": {
        "properties": {
            "title": {
                "type": "text",
                 "analyzer":"my_analyzer" 
                }
            }
     }
}
````

````text
POST analyzer-index/_doc/1
````
````json
{
"title": "HELLO my1 name is K3ev1in Sh1ind3el! N3ic3e!" 
}
````