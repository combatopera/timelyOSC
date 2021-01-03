# timelyOSC
Open Sound Control library for Python 3

## Install
These are generic installation instructions.

### To use, permanently
The quickest way to get started is to install the current release from PyPI:
```
pip3 install --user timelyOSC
```

### To use, temporarily
If you prefer to keep .local clean, install to a virtualenv:
```
python3 -m venv venvname
venvname/bin/pip install timelyOSC
. venvname/bin/activate
```

### To develop
First clone the repo using HTTP or SSH:
```
git clone https://github.com/combatopera/timelyOSC.git
git clone git@github.com:combatopera/timelyOSC.git
```
Now use pyven's pipify to create a setup.py, which pip can then use to install the project editably:
```
python3 -m venv pyvenvenv
pyvenvenv/bin/pip install pyven
pyvenvenv/bin/pipify timelyOSC

python3 -m venv venvname
venvname/bin/pip install -e timelyOSC
. venvname/bin/activate
```
