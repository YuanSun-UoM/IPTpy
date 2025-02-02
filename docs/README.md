# Using Read the Docs to generate the webpage

**Install Sphinx and Create Documentation**

- /opt/homebrew/bin/python3.11 is the Python path in the author's PC

```
/opt/homebrew/bin/python3.11 -m pip install sphinx
/opt/homebrew/bin/python3.11 -m pip install sphinx-book-theme

cd /Users/user/Desktop/YuanSun-UoM/IPTpy/docs/
sphinx-quickstart

> Separate source and build directories (y/n) [n]:
> Project name: IPTpy
> Author name(s): Yuan Sun, Zhonghua Zheng
> Project release []: 'v0.0.0'
> Project language [en]:
```

**Build HTML Files Locally**

```
sphinx-build -b html docs docs/_build
```

## Management

- [ReadTheDocs](https://app.readthedocs.org/), log in with the author's Github account.

