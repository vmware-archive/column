# Copyright (c) 2017 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0

.PHONY: tests-pep8 tests-python27 tests-coverage

tests-pep8:
	cd ..; tox -v -epep8;

tests-python27:
	cd ..;\
	tox -v -epy27;\
	status=$$?;\
	echo "Begin pip freeze output from test virtualenv:";\
	echo "======================================================================";\
	.tox/py27/bin/pip freeze;\
	echo "======================================================================";\
	if [ $$status -ne 0 ];\
	then \
	    false ;\
	fi

tests-coverage:
	cd ..; tox -v -ecover;
