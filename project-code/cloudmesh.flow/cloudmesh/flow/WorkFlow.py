#!/usr/bin/python
import sys
import re
from pprint import pprint
from cloudmesh.mongo.CmDatabase import CmDatabase
from cloudmesh.flow.Node import Node
from cloudmesh.mongo.DataBaseDecorator import DatabaseUpdate
from lark import Lark
from lark.tree import pydot__tree_to_png

grammar = """
    node: /[a-zA-Z]+/
    sequence: ";"
    parallel: "||"
    join: sequence | parallel
    expr: node join node | group | node
    group: "(" expr ")" | expr join expr

    %import common.WS
    %ignore WS
"""

parser = Lark(grammar, start = "expr")

class WorkflowDB(object):

    def __init__(self, name="workflow"):
        self.database = CmDatabase()
        self.workflow_name = name
        self.collection = self.database.collection(f"{name}-flow")

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

    def add_edge(self, node, depends_on):
        pprint(depends_on.name)
        self.collection.update_one({"name" : node.name}, {"$push" : {"dependencies" : depends_on.name}})

    def get_node(self, name=None):
        return self.collection.find_one({"name" : name})

    def list(self, node=None, edge=None):
        return self.collection.find({})

    def find_root_nodes(self):
        return self.collection.find({"dependencies.0" : {"$exists" : False}})

    def resolve_node_dependency(self, name=None):
        return self.collection.update_many({"dependencies" : name}, {"$pull" : {"dependencies" : name}})

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
        pprint(nodes)
        flow_nodes = []
        self.database = WorkflowDB(name)
        self.name = name
        self.node_names = []
        for node in nodes:
            node_name = node.replace(" ", "")
            flow_node = Node(node_name)
            self.node_names.append(node_name)
            flow_node.workflow = name
            print(flow_node)
            flow_nodes.append(flow_node)
            self.database.add_node(flow_node.toDict())
        for token in flowstring.split(" "):
            if token in self.node_names:
                print("token is a node", token)
            else:
                print("token is an edge", token)
        self.database.add_edge(flow_nodes[0], flow_nodes[1])
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
    flowstring = sys.argv[2]
    flowname = sys.argv[1]
    tree = parser.parse(flowstring)
    print(tree.pretty())
    pydot__tree_to_png(tree, "ee.png")
    #flow = WorkFlow(flowname, flowstring)
    # print(flow)
    # flow.run()

    #w = WorkflowDB("workflow01")
    #node = {"name": "world"}
    #w.add_node(node)
