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
from cloudmesh.flow import Node

import pytest

@pytest.mark.incremental
class Test_flowdb:

    def tearDown(self):
        pass

    @pytest.fixture(scope="session")
    def db(self):
        return WorkFlowDB("test")
    def test_create( db):
        assert 0, db

    def test_add_node(db):
        test_node = Node("test test")
        db.add_node(test_node)
        num_nodes = db.collection.count()
        assert num_nodes == 1

    def test_add_edge(db):
        node_1 = Node("testsource")
        node_2 = Node("testdest")
        db.add_node(node_1)
        db.add_node(node_2)
        db.add_edge(node_1.name, node_2.name)
        deps = db.collection.count({"dependencies.0" : {"$exists" : True}})
        assert deps == 1