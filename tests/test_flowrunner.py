###############################################################
# pip install .; pytest -v --capture=no -v --nocapture tests/test_flowrunner..py::Test_flowrunner.test_001
# pytest -v --capture=no tests/test_flowrunner.py
# pytest -v  tests/test_flowrunner.py
###############################################################
import os

from cloudmesh.common.ConfigDict import ConfigDict
from cloudmesh.common.util import HEADING
from cloudmesh.flow import FlowRunner

import pytest

@pytest.mark.incremental
class Test_flowrunner:

    # noinspection PyPep8Naming
    def tearDown(self):
        pass

    def test_create(self):
        runner = FlowRunner("test")

    def test_run(self):
        runner = FlowRunner("test")
        runner.start_flow()
        assert runner.running == True
