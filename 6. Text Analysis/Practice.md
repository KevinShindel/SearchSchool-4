# TASK DESCRIPTION

- Create custom non-English analyzer for html based documents.
- Make sure that Roman numbers are replaced as is with it’s Arabic numbers variation.

# TODO: Create logic 

1. Add text
````json
{
  "tokenizer": "standard",
  "text": "<b>Je m’appelle Jessica</b>"
}
````

````json
{
  "tokens": [
    {
      "token": "b",
      "start_offset": 1,
      "end_offset": 2,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "Je",
      "start_offset": 3,
      "end_offset": 5,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "m’appelle",
      "start_offset": 6,
      "end_offset": 15,
      "type": "<ALPHANUM>",
      "position": 2
    },
    {
      "token": "Jessica",
      "start_offset": 16,
      "end_offset": 23,
      "type": "<ALPHANUM>",
      "position": 3
    },
    {
      "token": "b",
      "start_offset": 25,
      "end_offset": 26,
      "type": "<ALPHANUM>",
      "position": 4
    }
  ]
}
````

2. Add HTML filter
````json
{
  "tokenizer": "standard",
  "text": "<b>Je m’appelle Jessica</b>",
  "char_filter" : ["html_strip"]
}
````
````json
{
  "tokens": [
    {
      "token": "Je",
      "start_offset": 3,
      "end_offset": 5,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "m’appelle",
      "start_offset": 6,
      "end_offset": 15,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "Jessica",
      "start_offset": 16,
      "end_offset": 27,
      "type": "<ALPHANUM>",
      "position": 2
    }
  ]
}
````

3. Add language


4. Romain number replace

5. Create Index with Tokenizer
````text
PUT /tokenizer_index
````
````json
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_custom_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "char_filter": [
            "html_strip"
          ],
          "filter": [
            "lowercase",
            "asciifolding",
            "roman_letters_synonyms"
          ]
        }
      },
      "filter": {
        "roman_letters_synonyms": {
          "type": "synonym_graph",
          "synonyms": [
            "18 => XVIII"
          ]
        }
      }
    }
  }
}
````
6. Test analyzer endpoint
````text
POST /tokenizer_index/_analyze
````
````json
{
  "analyzer": "my_custom_analyzer",
  "text": "Is this <b>déjà vu</b>?"
}
````

7. Create new document
````text
POST /tokenizer_index/_doc
````
````json
{
  "name": "<b>Je m’appelle Jessica</b>\n <small>Le trajet ne dure que XVIII minutes !</small>\n"
}
````
