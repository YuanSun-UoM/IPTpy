# Using Read the Docs to generate the webpage

- https://app.readthedocs.org/, log in with author's Github account.

**Install Sphinx and Create Documentation**

- /opt/homebrew/bin/python3.11 is the Python path in author's PC

```
/opt/homebrew/bin/python3.11 -m pip install sphinx
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
sphinx-build -b html docs/source docs/build
```

