# phrase extractor

A shallow phrase extractor based on nltk 


## Installation

```
pip3 install phraseextractor
```

### Example

```python

from extractor import phrases_extractor

text = ('GOP Sen. Rand Paul was assaulted in his home in Bowling Green, Kentucky, on Friday, '
        'according to Kentucky State Police. State troopers responded to a call to the senator\'s '
        'residence at 3:21 p.m. Friday. Police arrested a man named Rene Albert Boucher, who they '
        'allege "intentionally assaulted" Paul, causing him "minor injury". Boucher, 59, of Bowling '
        'Green was charged with one count of fourth-degree assault. As of Saturday afternoon, he '
        'was being held in the Warren County Regional Jail on a $5,000 bond.')

grammar = r"""
        NP:   {<NNP>?<NNP>?}
    """

label = 'NP'

terms = phrases_extractor.get_phrases(text,grammar,label)
```
