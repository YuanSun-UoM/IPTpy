# Installation
------

Below are installation instructions for setting up via the command line in a bash environment. You can choose to manage the environment using either [venv (Python virtual environment)](https://docs.python.org/3/library/venv.html) or [Conda](https://docs.conda.io/projects/conda/en/latest/).

## Quick Installation

- Method1: install by [pip](https://pypi.org/project/pip/)

```
pip install iptpy
```

- Method2: install by Conda

```
conda install -c conda-forge iptpy
```

## Installation Step by Step

### Step 1: Check the Python path and virtual environment

- Check the Python path

```
which python3
```

- List and choose an existing virtual environment for installation

```
# choose an virtual environment in a specific folder
ls /path/to/venvs

# list Conda virtual environment and choose one
conda env list
```

- Or, create a new virtual environment for installation 

```
# for example, 'myenv' is the new virtual environment name
python3 -m venv myenv 

# or specify Python version when creating a new virtual environment
python3.9 -m venv myenv

# or create a Conda virtual environment
conda create -n myenv

# or create a Conda virtual environment with a specific version of Python
conda create -n myenv python=3.9

# or create a Conda virtual environment with a specific version of Python and packages
conda create -n myenv python=3.9 -c conda-forge numpy xarray pandas datetime netcdf4 xesmf iptpy
```

### Step 2: Install IPTpy

- Install IPTpy in a venv virtual environment

```
source myenv/bin/activate
pip install iptpy 
```

- Install IPTpy in a Conda virtual environment

```
conda activate myenv
conda install -c conda-forge iptpy
```

### Step 3: Verify installation

- For venv virtual environment:

```
pip show iptpy
```

- For Conda virtual environment:

```
conda list iptpy
```

### Step 4: Deactivation

- For venv virtual environment:

```
deactivate
```

- For Conda virtual environment

```
conda deactivate
```

