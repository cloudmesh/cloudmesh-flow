#!/usr/bin/python
import sys
import re
from pprint import pprint
from cloudmesh.mongo.CmDatabase import CmDatabase
from cloudmesh.flow.Node import Node
from cloudmesh.mongo.DataBaseDecorator import DatabaseUpdate
from lark import Lark, Visitor
from lark.tree import pydot__tree_to_png

grammar = """
    flownode: /[a-zA-Z]+/
    sequence: ";"
    parallel: "||"
    join: sequence | parallel
    expr:  group | flownode
    basegroup.1: flownode join flownode
    group: "(" expr ")" | basegroup | flownode join expr | expr join flownode | expr join expr

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
        self.collection.update_one({"name" : node}, {"$push" : {"dependencies" : depends_on}})

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

class FlowConstructor(Visitor):
    def flownode(self, val):
        print("node", val,  val.children[0])
        name = val.children[0]
        node = Node(name)
        node.workflow = self.flowname
        self.db.add_node(node.toDict())

    def join(self, val):
        join_type = val.children[0].data
        print("join", val.children, "as", join_type)

    def basegroup(self, val):
        print(val, len(val.children))
        #expressions are either a single node or a group
        if len(val.children) == 1: return
        lhs = val.children[0]
        join = val.children[1]
        rhs = val.children[2]
        join_type = join.children[0].data
        print("join of type", join_type)
        if join_type == "sequence":
            lhs_node_name = lhs.children[0]
            rhs_node_name = rhs.children[0]
            print("join", lhs_node_name, "with", rhs_node_name, "in type", join_type)
            self.db.add_edge(lhs_node_name, rhs_node_name)

if __name__ == "__main__":
    flowstring = sys.argv[2]
    flowname = sys.argv[1]
    tree = parser.parse(flowstring)
    print(tree.pretty())
    db = WorkflowDB(flowname)
    flow = FlowConstructor()
    flow.db = db
    flow.flowname = flowname
    flow.visit(tree)
        
    #pydot__tree_to_png(tree, "ee.png")

    #flow = WorkFlow(flowname, flowstring)
    # print(flow)
    # flow.run()

    #w = WorkflowDB("workflow01")
    #node = {"name": "world"}
    #w.add_node(node)
