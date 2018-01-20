![Column](https://github.com/vmware/column/blob/master/column.png "Column")

[![Build Status](https://travis-ci.org/vmware/column.svg?branch=master)](https://travis-ci.org/vmware/column)
[![codecov](https://codecov.io/gh/vmware/column/branch/master/graph/badge.svg)](https://codecov.io/gh/vmware/column)
[![Latest Version](https://img.shields.io/pypi/v/column.svg)](https://pypi.python.org/pypi/column/)
[![Python Versions](https://img.shields.io/pypi/pyversions/column.svg)](https://pypi.python.org/pypi/column/)
[![Format](https://img.shields.io/pypi/format/column.svg)](https://pypi.python.org/pypi/column/)
[![License](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://github.com/vmware/column/blob/master/LICENSE)

## Overview
Column is a thin wrapper on top of the Ansible API to serve
as an entry point for other code when Ansible is needed. Because the Ansible
internal API is not officially exposed and changes frequently, this wrapper
can be used instead of touching Ansible directly so that any further Ansible
API changes will only incur change in this module.

This module exposes two classes:
column.APIRunner and column.SubprocessRunner

Both of these implement the API as described in column.Runner.
Each runner exposes two public methods:
run_playbook() and run_module().

## Try it out

### Prerequisites
* python 2.7 (python 3 is not fully supported by ansible)
* ansible 2.x
* six library

### Install & use
Install with pip:
```bash
pip install column
```
and in your python code do:
```python
from column import APIRunner
api_runner = APIRunner()
api_runner.run_module('localhost', remote_user=None)
```
## Running the API
```bash
python column/api/run.py
```

## Running the API in uWSGI
```bash
pip install uwsgi
uwsgi --socket 0.0.0.0:48620 --protocol=http -w column.api.wsgi
```

## Running in Docker
```docker
1. docker build -t column-image .
2. docker run -d -p 48620:48620 -v <playbook-dir>:<container-dir> column-image (the directory should contain the playbook file)
```

## Documentation
TBD

## Releases & Major Branches
Column is still in alpha state, currently at version 0.5.2.

## Contributing

The Column project team welcomes contributions from the community. Before you start working with Column, please read our [Developer Certificate of Origin](https://cla.vmware.com/dco). All contributions to this repository must be signed as described on that page. Your signature certifies that you wrote the patch or have the right to pass it on as an open-source patch. For more detailed information, refer to [CONTRIBUTING.md](CONTRIBUTING.md).
