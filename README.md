# Column

* A stable API for Ansible *

## Introduction
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

## Installing
TBD

## Examples
TBD

## Contribution guidelines

Contribution and feature requests are more than welcome. Please use the following methods:

* For bugs and feature requests, use GitHub issues feature. register with details of the problem or specifics of requested feature.
* For code contribution (bug fixes, or feature request), please fork Column, create a feature branch, push your code, then submit a pull request.

## License

Column 0.2.0

Copyright © 2017 VMware, Inc.  All rights reserved.

The BSD-2 license (the "License") set forth below applies to all parts of the VMware Column 0.2.0
project. You may not use this file except in compliance with the License.

BSD-2 License

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.