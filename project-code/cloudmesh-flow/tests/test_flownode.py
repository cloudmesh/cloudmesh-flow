###############################################################
# pip install .; pytest -v --capture=no -v --nocapture tests/test_flownode.py:Test_flownode.test_001
# pytest -v --capture=no tests/test_flownode.py
# pytest -v  tests/test_flownode.py
###############################################################

from __future__ import print_function

import os

from cloudmesh.common.ConfigDict import ConfigDict
from cloudmesh.common.util import HEADING
import pytest

@pytest.mark.incremental
class Test_flownode:

    # noinspection PyPep8Naming
    def tearDown(self):
        pass

    def test_create(self):
        a = 1
        print()
        print("hello world",a)
        print()
        assert a==1 
