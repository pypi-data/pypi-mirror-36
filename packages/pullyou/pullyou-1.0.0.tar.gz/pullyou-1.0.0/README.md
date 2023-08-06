PullYou is a tool for opening the PR associated with a given git hash.

Releasing
-------------
```
$ python setup.py sdist bdist_wheel
$ twine upload dist/* [-r testpypi]
$ rm -rf dist/*
* tag the release
* bump the version number
```
