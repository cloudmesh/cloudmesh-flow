###############################################################
# pip install .; pytest -v --capture=no -v --nocapture tests/test_flownode.py:Test_flownode.test_001
# pytest -v --capture=no tests/test_flownode.py
# pytest -v  tests/test_flownode.py
###############################################################

from __future__ import print_function

import os

from cloudmesh.common.ConfigDict import ConfigDict
from cloudmesh.common.util import HEADING
from cloudmesh.flow.Node import Node

import pytest

@pytest.mark.incremental
class Test_flownode:

    # noinspection PyPep8Naming
    def tearDown(self):
        pass

    def test_create(self):
       mynode = Node("test")

    def test_get_command(self):
        mynode = Node("test2")
        comm_arr = mynode.get_command()
        mynode.workflow = "test2"
        assert comm_arr[0] == "python"
        assert comm_arr[1] == "test2-flow.py"
        assert comm_arr[2] == "test2"

    def test_add_dep(self):
        node_1 = Node("node1")
        node_2 = Node("node2")
        node_1.add_dependency(node_2)
        assert len(node_1.dependencies) == 1


