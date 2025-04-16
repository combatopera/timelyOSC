# timelyOSC
Open Sound Control library for Python 3.

## Install
These are generic installation instructions.

### To use, disposably
Install the current release from PyPI to a virtual environment:
```
python3 -m venv venvname
venvname/bin/pip install -U pip
venvname/bin/pip install timelyOSC
. venvname/bin/activate
```

### To use, permanently
```
pip3 install --break-system-packages --user timelyOSC
```
See `~/.local/bin` for executables.

### To develop
First install venvpool to get the `motivate` command:
```
pip3 install --break-system-packages --user venvpool
```
Get codebase and install executables:
```
git clone git@github.com:combatopera/timelyOSC.git
motivate timelyOSC
```
Requirements will be satisfied just in time, using sibling projects with matching .egg-info if any.

## API

<a id="timelyOSC"></a>

### timelyOSC

