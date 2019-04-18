###############################################################
# pip install .; pytest -v --capture=no -v --nocapture tests/test_flowdb.py:Test_flowdb.test_001
# pytest -v --capture=no tests/test_flowdb.py
# pytest -v  tests/test_flowdb.py
###############################################################

from __future__ import print_function

import os

from cloudmesh.common.ConfigDict import ConfigDict
from cloudmesh.common.util import HEADING
from cloudmesh.flow.WorkFlow import WorkFlowDB
from cloudmesh.flow.Node import Node

import pytest

@pytest.mark.incremental
class Test_flowdb:

    def tearDown(self):
        pass

    def setup(self):
        self.db = WorkFlowDB("test")

    def test_add_node(self):
        test_node = Node("test test")
        self.db.add_node(test_node.toDict())
        num_nodes = self.db.collection.count()
        assert num_nodes == 1

    def test_add_edge(self):
        node_1 = Node("testsource")
        node_2 = Node("testdest")
        self.db.add_node(node_1.toDict())
        self.db.add_node(node_2.toDict())
        self.db.add_edge(node_1.name, node_2.name)
        deps = self.db.collection.count({"dependencies.0" : {"$exists" : True}})
        assert deps == 1