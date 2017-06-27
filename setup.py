#!/usr/bin/env python

# Copyright (c) 2017 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause


"""
column is a thin wrapper on top of ansible API, to serve
as an entry point for other code when ansible is needed. As ansible
internal API is not officially exposed and thus changes are very likely,
this wrapper should be used instead of touching ansible directly,
so that any further ansible API change will only incur change in this module.

It exposes two classes:
column.APIRunner and column.SubprocessRunner

Both of them implement API described in column.Runner.
Each runner expose two public methods:
run_playbook() and run_module().
"""


from setuptools import setup

setup(
    name='column',
    version='0.3.5',
    url='https://github.com/vmware/column',
    license='BSD-2',
    author='VMware',
    author_email='openstack@vmware.com',
    description='A thin wrapper on top of ansible with a stable API.',
    long_description=__doc__,
    packages=['column'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=open('requirements.txt').read().splitlines(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Operating System :: POSIX :: Linux',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
    ]
)
