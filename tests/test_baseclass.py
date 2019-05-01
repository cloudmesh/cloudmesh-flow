###############################################################
# pip install .; pytest -v --capture=no -v --nocapture tests/test_baseclass.py:Test_baseclass.test_001
# pytest -v --capture=no tests/test_baseclass.py
# pytest -v  tests/test_baseclass.py
###############################################################


from __future__ import print_function

import os

from cloudmesh.common.ConfigDict import ConfigDict
from cloudmesh.common.util import HEADING
from cloudmesh.flow.FlowDecorator import BaseWorkFlow
from cloudmesh.flow.WorkFlow import WorkFlowDB
import pytest

class SampleFlow(BaseWorkFlow):
    def a(self):
        return {"name" : "a", "result" : {"everything" : "ok"}}

@pytest.mark.incremental
class Test_baseclass:
    # noinspection PyPep8Naming
    def tearDown(self):
        pass

    def setup(self):
        self.db = WorkFlowDB("test")
        self.db.collection.delete_many({})
        self.db.add_node({"name" : "a", "dependencies" : []})
        self.db.start_flow()
        self.flow = SampleFlow("test-flow.py")


    def test_runmethod(self):
        result = self.flow.runCommand("a")
        assert result["name"] == "a"

    def test_database_insertion(self):
        result = self.flow.runCommand("a")
        dbresult = self.db.get_node("a")
        assert dbresult["result"]["name"] == "a"
        assert dbresult["result"]["result"]["everything"] == "ok"