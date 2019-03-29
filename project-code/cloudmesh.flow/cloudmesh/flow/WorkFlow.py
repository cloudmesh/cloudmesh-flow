#!/usr/bin/python
import sys
import re
from cloudmesh.mongo.CmDatabase import CmDatabase
from cloudmesh.flow.Node import Node
from cloudmesh.mongo.DataBaseDecorator import DatabaseUpdate


class WorkflowDB(object):

    def __init__(self, name="workflow"):
        self.database = CmDatabase()
        self.workflow_name = name

    def attributes(self, name):
        data = {
            "cm": {
                "kind": "flow",
                "cloud": self.workflow_name,
                "name": name
            },
            "kind": "flow",
            "cloud": self.workflow_name,
            "name": name
        }
        return data

    @DatabaseUpdate()
    def add_node(self, node):
        name = node["name"]
        node.update(self.attributes(name))
        return node

    def add_edge(self, node):
        pass

    def node_node(self, name=None):
        pass

    def get_edge(self, name=None):
        pass

    def list(self, node=None, edge=None):
        pass

    def find_root_nodes(self):
        pass

    def resolve_node_dependency(self, name=None):
        pass

    def add_specification(self, spec):
        pass

    def add_graph(self, yamlfile):
        pass


class WorkFlow(object):
    def __init__(self, name, flowstring):

        self.SPLIT_CHARS = ["\|", "&", ";"]
        self.SPLIT_RE = re.compile("|".join(self.SPLIT_CHARS))

        self.flowstring = flowstring
        nodes = self.SPLIT_RE.split(flowstring)
        flow_nodes = []
        self.database = WorkflowDB()
        self.name = name
        for node in nodes:
            flow_node = Node(node)
            flow_node.workflow = name
            print(flow_node)
            flow_nodes.append(flow_node)
            self.database.add_node(flow_node.toDict())

    def __repr__(self):
        return " ".join([self.name, self.flowstring])

    def run(self):
        collection = self.database.collection("workflow")
        initial_nodes = collection.find(
            {"workflow": self.name, "dependencies.0": {"$exists": False}})
        for initial_node in initial_nodes:
            self.run_node(initial_node)

    def run_node(self, node):
        print("running node", node)


if __name__ == "__main__":
    # flowstring = sys.argv[1]
    # flow = WorkFlow("myflow", flowstring)
    # print(flow)
    # flow.run()

    w = WorkflowDB("workflow01")
    node = {"name": "world"}
    w.add_node(node)
