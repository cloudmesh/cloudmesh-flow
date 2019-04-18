###############################################################
# pip install .; pytest -v --capture=no -v --nocapture tests/test_flowdb.py:Test_flowdb.test_001
# pytest -v --capture=no tests/test_flowdb.py
# pytest -v  tests/test_flowdb.py
###############################################################

from __future__ import print_function

import os

from cloudmesh.common.ConfigDict import ConfigDict
from cloudmesh.common.util import HEADING
from cloudmesh.flow import WorkFlowDB

import pytest

@pytest.mark.incremental
class Test_flowdb:

    # noinspection PyPep8Naming
    def tearDown(self):
        pass

    def test_create(self):
        a = 1
        print()
        print("hello world",a)
        print()
        assert a==1 
