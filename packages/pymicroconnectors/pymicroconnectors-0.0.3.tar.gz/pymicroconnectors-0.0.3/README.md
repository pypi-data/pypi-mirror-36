# Py Micro Connectors

[![made-with-python](https://img.shields.io/badge/pypi-pymicroconnectors-green.svg?style=flat-square)](https://pypi.org/project/pymicroconnectors/)
[![licence](https://img.shields.io/badge/licence-MIT-green.svg?style=flat-square)](https://github.com/ddelizia/pymicroconnectors/LICENCE)


This is a simple example package. You can use
[Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/)
to write your content.


## Config

## Logger

Adding colored logs to the application in an easy and configurable way


```
import pymicroconnectors.logger as logger

logger.init()
```

## Ebay

```
import pymicroconnectors.ebay as ebay

logger.init()
```

### Dev Notes

```
python3 setup.py sdist bdist_wheel
twine upload dist/*
```
