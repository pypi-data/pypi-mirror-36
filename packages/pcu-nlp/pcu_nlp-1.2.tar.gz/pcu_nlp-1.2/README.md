# pcu_nlp

NLP pipeline component (spacy.io) for PCU project

Based on [spacy.io][spacy].

[Check PCU project][pcu].

[spacy]: https://spacy.io
[pcu]: https://github.com/zevio/pcu_core

----

## Installation

To install requirements, go to pcu_nlp/ directory and execute the Makefile with the following command line :

`make init`

## Usage in another project

If you wish to import this module in another Python project, please install it :

`pip install pcu-nlp`

Then, add this import line at the beginning of your Python file :

`from pcu_nlp import pcu_nlp`

You can now use pcu_nlp's functions, for example :

`pcu_nlp.spacyPipeline(text)`

## Test

To test your installation, go to pcu_nlp/ directory and execute the Makefile with the following command line : 

`make test`
