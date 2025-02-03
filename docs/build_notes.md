# Create virtual environment for testing

```
conda create --name testingenv python=3.11
conda activate testingenv
conda install sphinx-book-theme sphinx-markdown-tables recommonmark nbconvert nbsphinx sphinx myst-nb
pip install sphinx_design
```

- install IPTpy locally

```
pip install -e /Users/user/Desktop/YuanSun-UoM/IPTpy

# verify installation
conda list iptpy
```



# Using Read the Docs to generate the webpage

**Install Sphinx and Create Documentation**

```
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
cd /Users/user/Desktop/YuanSun-UoM/IPTpy
sphinx-build -b html docs/ docs/_build

# open the html
open /Users/user/Desktop/YuanSun-UoM/IPTpy/docs/_build/index.html
```

# Management

- [ReadTheDocs](https://app.readthedocs.org/), log in with the author's Github account. It keeps updating with the GitHub commit. 

- For GitHub, enable **Discussions** and add **issue templates** through the **Settings**.
- 