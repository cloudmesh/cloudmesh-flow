#!/usr/bin/python
import sys
import re
from pprint import pprint
from cloudmesh.mongo.CmDatabase import CmDatabase
from cloudmesh.flow.Node import Node
from cloudmesh.mongo.DataBaseDecorator import DatabaseUpdate
from lark import Lark, Visitor
from lark.tree import pydot__tree_to_png
import oyaml as yaml
from cloudmesh.DEBUG import VERBOSE


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

class WorkFlowDB(object):

    def __init__(self, name="workflow", active = False):
        self.database = CmDatabase()
        self.workflow_name = name
        self.collection = self.database.collection(f"{name}-flow")
        if active:
            self.switch_to_active_flow()

    def attributes(self, name):
        data = {
            "cm": {
                "kind": "flow",
                "cloud": self.workflow_name,
                "name": name
            },
            "kind": "flow",
            "cloud": self.workflow_name,
            "name": name,
            "status" : "defined"
        }
        return data

    @DatabaseUpdate()
    def add_node(self, node):
        name = node["name"]
        node.update(self.attributes(name))
        VERBOSE(node)
        return node

    def add_edge(self, node, depends_on):
        edge = {
            "node": node,
            "depends_on": depends_on
        }
        VERBOSE(edge)
        self.collection.update_one(
            {"name" : node},
            {"$push" : {"dependencies" : depends_on}})

    def _node_from_db(self, db_obj):
        reconstructed = Node(db_obj["name"])
        reconstructed.workflow = self.workflow_name
        reconstructed.dependencies = db_obj["dependencies"]
        reconstructed.status = db_obj.get("status", "pending")
        reconstructed.result = db_obj.get("result", {})
        return reconstructed

    def remove_node(self, name):
        self.collection.delete_one({"name" : name})
        self.collection.update_many({}, {"$pull" : {"dependencies" : "name"}})

    def remove_edge(self, node, depends_on):
        self.collection.update_one({"name" : node}, {"$pull" : {"dependencies" : depends_on}})

    def get_node(self, name=None):
        return self._node_from_db(self.collection.find_one({"name" : name}))

    def list(self, node=None, edge=None):
        query = {}
        if node:  query["name"] = node
        if edge: query["dependencies"] = edge
        return self.collection.find(query)

    def list_nodes(self):
        return [self._node_from_db(node) for node in self.list()]

    def list_edges(self):
        return self.collection.aggregate(
            [{"$unwind" : "$dependencies"},
             {"$project" : {"to" : "$name", "from" : "$dependencies"}}])

    def list_all_workflows(self):
        all_colls = self.database.collections()
        return [name for name in all_colls if "flow" in name and "active" not in name]
    
    def set_node_status(self, node, status):
        return self.collection.update_one(
            {"name" : node}, {"$set" : {"status" : status}})

    def find_root_nodes(self):
        root_nodes = self.collection.find(
            {"dependencies.0" : {"$exists" : False}, "status" : "pending"})
        return [self._node_from_db(node) for node in root_nodes]
    
    def switch_to_active_flow(self):
        started_collection = f"{self.workflow_name}-flow-active"
        self.collection = self.database.collection(started_collection)

    def resolve_node_dependencies(self, name=None):
        return self.collection.update_many(
            {"dependencies" : name}, {"$pull" : {"dependencies" : name}})

    def add_specification(self, spec):
        pass

    def start_flow(self):
        VERBOSE("START")
        started_collection = f"{self.workflow_name}-flow-active"
        self.collection.aggregate([
            {"$project" : {
                "dependencies" :1,
                "cm" :1,
                "kind" : 1,
                "cloud" : 1,
                "name" : 1,
                "status" : "pending"}},
            {"$out" : started_collection}])
        self.switch_to_active_flow()


    def add_node_result(self, nodename, result):
        return self.collection.update_one({"name" : nodename}, {"$set" : {"result" : result}})

    def add_graph(self, yamlfile):
        pass

    def last_update(self, workflow=None):
        """
        This method returns the last modified value associated with a
        database update to a node.

        :param workflow: The name of the workflow
        :type workflow: string
        :return: The time of the last update
        :rtype: string
        """
        raise NotImplementedError
        t = "the time string"
        return t


class FlowConstructor(Visitor):
    def flownode(self, val):
        name = val.children[0]
        node = Node(name)
        node.workflow = self.flowname
        self.db.add_node(node.toDict())

    def join(self, val):
        join_type = val.children[0].data
        #print("join", val.children, "as", join_type)

    def basegroup(self, val):
        #print(val, len(val.children))
        #expressions are either a single node or a group
        if len(val.children) == 1: return
        lhs = val.children[0]
        join = val.children[1]
        rhs = val.children[2]
        join_type = join.children[0].data
        #print("join of type", join_type)
        if join_type == "sequence":
            lhs_node_name = lhs.children[0]
            rhs_node_name = rhs.children[0]
            #print("join", lhs_node_name, "with", rhs_node_name, "in type", join_type)
            self.db.add_edge(rhs_node_name, lhs_node_name)

    def group(self, val):
        if len(val.children) == 1: return
        lhs = val.children[0]
        join = val.children[1]
        rhs = val.children[2]
        join_type = join.children[0].data
        lhs_node = self.resolve_to_node(lhs)
        rhs_node = self.resolve_to_node(rhs)
        if join_type == "sequence":
            lhs_node_name = lhs_node.children[0]
            rhs_node_name = rhs_node.children[0]
            #print("join", lhs_node_name, "with", rhs_node_name, "in type", join_type)
            self.db.add_edge(rhs_node_name, lhs_node_name)

    def _is_node(self, val):
        #print("is node", val.data)
        return val.data == "flownode"

    def resolve_to_node(self, val):
        if self._is_node(val): return val
        else:
            #print(val.data, val.children)
            return self.resolve_to_node(val.children[-1])



def parse_string_to_workflow(flowstring, flowname):
    tree = parser.parse(flowstring)
    db = WorkFlowDB(flowname)
    flow = FlowConstructor()
    flow.db = db
    flow.flowname = flowname
    flow.visit(tree)

def parse_yaml_to_workflow(yaml_file):
    with open(yaml_file) as yaml_contents:
        data = yaml.load(yaml_contents, Loader=yaml.SafeLoader)
        flowstring = data["flow"]
        flowname = data["name"]
        return parse_string_to_workflow(flowstring, flowname)


if __name__ == "__main__":
    flowstring = sys.argv[2]
    flowname = sys.argv[1]
    db = WorkFlowDB()
    flows = db.list_all_workflows()
    for flow in flows:
        print(flow)
    parse_string_to_workflow(flowstring, flowname)
    
    #pydot__tree_to_png(tree, "ee.png")

    #flow = WorkFlow(flowname, flowstring)
    # print(flow)
    # flow.run()

    #w = WorkFlowDB("workflow01")
    #node = {"name": "world"}
    #w.add_node(node)
