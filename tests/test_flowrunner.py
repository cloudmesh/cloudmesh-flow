###############################################################
# pip install .; pytest -v --capture=no -v --nocapture tests/test_flowrunner.py:Test_flowrunner.test_001
# pytest -v --capture=no tests/test_flowrunner.py
# pytest -v  tests/test_flowrunner.py
###############################################################

from __future__ import print_function

import os

from cloudmesh.common.ConfigDict import ConfigDict
from cloudmesh.common.util import HEADING
from cloudmesh.flow import WorkflowRunner

import pytest

@pytest.mark.incremental
class Test_flowrunner:

    # noinspection PyPep8Naming
    def tearDown(self):
        pass

    def test_create(self):
        runner = WorkflowRunner("test")

    def test_run(self):
        runner = WorkflowRunner("test")
        runner.start_flow()