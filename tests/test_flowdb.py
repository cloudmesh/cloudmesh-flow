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
        self.db.collection.delete_many({})

    def test_add_node(self):
        test_node = Node("test test")
        self.db.add_node(test_node.toDict())
        num_nodes = self.db.collection.count_documents()
        assert num_nodes == 1

    def test_add_edge(self):
        node_1 = Node("testsource")
        node_2 = Node("testdest")
        self.db.add_node(node_1.toDict())
        self.db.add_node(node_2.toDict())
        self.db.add_edge(node_1.name, node_2.name)
        deps = self.db.collection.count_documents({"dependencies.0" : {"$exists" : True}})
        assert deps == 1

    def test_set_node_status(self):
        node_name = "status_test"
        status = "testing"
        node_1 = Node(node_name)
        self.db.add_node(node_1.toDict())
        inserted_node = self.db.get_node(node_name)
        print(inserted_node.status)
        self.db.set_node_status(node_name, status)
        reset_node = self.db.get_node(node_name)
        assert reset_node.status == status

    def test_start_flow(self):
        self.db.collection.delete_many({})
        node_1 = Node("node1")
        node_2 = Node("node2")
        node_3 = Node("node3")
        node_1.add_dependency(node_2)
        for node in [node_1, node_2, node_3]:
            self.db.add_node(node.toDict())
        self.db.start_flow()
        new_collection = self.db.collection
        print(new_collection)
        new_nodes = self.db.list_nodes()
        for node in new_nodes:
            print(node.status)
            assert node.status == "pending"


    def test_remove(self):
        self.db.collection.remove_many({})
        node_1 = Node("testsource")
        node_2 = Node("testdest")
        self.db.add_node(node_1.toDict())
        self.db.add_node(node_2.toDict())
        self.db.add_edge(node_1.name, node_2.name)
        deps = self.db.collection.count_documents({"dependencies.0" : {"$exists" : True}})
        assert deps == 1
        self.db.remove_edge(node_1.name, node_2.name)
        deps = self.db.collection.count_documents({"dependencies.0" : {"$exists" : True}})
        assert deps == 0
        self.db.remove_node(node_1.name)
        nodes = self.db.collection.count_documents({"name" : node_1.name})
        assert nodes == 0
