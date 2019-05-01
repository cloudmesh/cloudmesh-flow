###############################################################
# pytest -v --capture=no benchmark/benchmark_ingest.py
# pytest -v  benchmark/benchmark_ingest.py
# pytest -v --capture=no benchmark/test_cms.py:Test_cms.<METHIDNAME>
###############################################################
import os
import sys
import platform

import pytest
from cloudmesh.DEBUG import VERBOSE
from cloudmesh.common.Printer import Printer
from cloudmesh.common.Shell import Shell
from cloudmesh.common.StopWatch import StopWatch
from cloudmesh.common.util import HEADING
from cloudmesh.common.systeminfo import systeminfo
from pprint import pprint

num_nodes = 50
@pytest.mark.incremental
class TestConfig:
    def test_add_nodes(self):
        HEADING()

        StopWatch.start("add nodes")
        results = []

        for node in range(num_nodes):
            node_name = f"node{str(node)}"
            results.append(Shell.execute("cms flow node add "  + node_name, shell=True))
        StopWatch.stop("add nodes")
        VERBOSE(results)


    def test_add_edges(self):
        HEADING()

        StopWatch.start("add edges")
        results = []

        for node in range(num_nodes - 1):
            node_name = f"node{str(node)}"
            next_node_name = f"node{str(node + 1)}"
            results.append(Shell.execute("cms flow edge add " + node_name + " " + next_node_name, shell=True))

        StopWatch.stop("add edges")

        VERBOSE(result)

    def test_remove_edges(self):
        HEADING()

        StopWatch.start("del edges")
        results = []

        for node in range(num_nodes - 1):
            node_name = f"node{str(node)}"
            next_node_name = f"node{str(node + 1)}"
            results.append(Shell.execute("cms flow edge delete " + node_name + " " + next_node_name, shell=True))
        StopWatch.stop("del edges")

        VERBOSE(result)

    def test_remove_nodes(self):
        HEADING()

        StopWatch.start("del nodes")
        results = []

        for node in range(num_nodes):
            node_name = f"node{str(node)}"
            results.append(Shell.execute("cms flow node remove "  + node_name, shell=True))
        StopWatch.stop("del nodes")
        VERBOSE(results)
