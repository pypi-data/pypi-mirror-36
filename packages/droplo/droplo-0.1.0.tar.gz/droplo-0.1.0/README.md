droplo.py
=========

## Python client for the [Droplo](https://droplo.io) content API

[![Latest PyPI version](https://img.shields.io/pypi/v/droplo.py.svg)](https://pypi.python.org/pypi/droplo.py)

[![MIT License](https://img.shields.io/badge/license-MIT-brightgreen.svg)](LICENSE)

### Getting started

#### Install the client for your project

Simply run:

```
pip install droplo
```

#### Basic example of use:
```python
>>> import droplo
>>> api = droplo.get("YOUR_ACCESS_TOKEN")
>>> blogposts = api.get("blogposts")
>>> blogposts.files[0].name
```

#### Using Memcached (or any other cache)

By default, the kit will use Shelve to cache the requests (a file-based cache from the standard library). It is recommended to use a cache server instead, for example Memcached.

You can pass a Memcached client to the `droplo.get` call:

```python
>>> import memcache
>>> api = droplo.get("YOUR_ACCESS_TOKEN", cache=memcache.Client(['127.0.0.1:11211']))
```

By duck typing you can pass any object that implement the `set` and `get` methods (see the `NoCache` object for the methods
to implement).

### Licence

Copyright (c) 2018 Droplo, Inc. See [LICENSE](License) for further details.
