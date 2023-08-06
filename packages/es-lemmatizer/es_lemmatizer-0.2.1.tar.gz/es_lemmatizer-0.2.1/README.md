# Spanish lemmatizer

Read data/LICENSE first

## Install it

    pip install es-lemmatizer

## How to use it:

```
from es_lemmatizer import lemmatize
import spacy
nlp = spacy.load("es")
nlp.add_pipe(lemmatize, after="tagger")
```


## How to publish:

```
rm -rf dist
python setup.py clean --all
python setup.py sdist bdist_wheel
twine upload --repository-url https://test.pypi.org/legacy/ --verbose dist/*
```