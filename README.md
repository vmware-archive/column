![Column](https://github.com/vmware/column/blob/master/column.png "Column")

[![Build Status](https://travis-ci.org/vmware/column.svg?branch=master)](https://travis-ci.org/vmware/column)
[![License](https://img.shields.io/badge/License-BSD%202--Clause-orange.svg)](https://github.com/vmware/column/blob/master/LICENSE)

## Overview
Column is a thin wrapper on top of ansible API, to serve
as an entry point for other code when ansible is needed. As the ansible
internal API is not officially exposed and thus changes are very likely,
this wrapper should be used instead of touching ansible directly,
so that any further ansible API change will only incur change in this module.

It exposes two classes:
column.APIRunner and column.SubprocessRunner

Both of them implement API described in column.Runner.
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

## Documentation
TBD

## Releases & Major Branches
Column is still in alpha state, currently at version 0.3.5.

## Contributing

The Column project team welcomes contributions from the community. Before you start working with Column, please read our [Developer Certificate of Origin](https://cla.vmware.com/dco). All contributions to this repository must be signed as described on that page. Your signature certifies that you wrote the patch or have the right to pass it on as an open-source patch. For more detailed information, refer to [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Column 0.3.5

Copyright © 2017 VMware, Inc.  All rights reserved.

The BSD-2 license (the "License") set forth below applies to all parts of the VMware Column 0.3.5
project. You may not use this file except in compliance with the License.

BSD-2 License

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
