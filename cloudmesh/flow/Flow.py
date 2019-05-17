#!/usr/bin/python
import sys
from cloudmesh.mongo.CmDatabase import CmDatabase
from cloudmesh.flow.Node import Node
from cloudmesh.mongo.DataBaseDecorator import DatabaseUpdate
from lark import Lark, Visitor
import oyaml as yaml
from cloudmesh.common.debug import VERBOSE
import inspect
from cloudmesh.common.console import Console

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

class Get:

    @staticmethod
    def nodes(classname):
        names = []
        method_list = [func for func in dir(classname) if callable(getattr(classname, func))]
        for name in method_list:
            if name.startswith("_"):
                pass
            else:
                names.append(name)
        return names

    @staticmethod
    def name(classname):
        s = classname.__name__
        return f"{s}" # flow will be appended later

    @staticmethod
    def edges(classname):
        return classname.edges

class Put:

    @staticmethod
    def nodes(name, nodes):

        db = FlowDatabase(name)

        for node in nodes:
            node = Node(node)
            node.workflow = name
            try:
                db.add_node(node.toDict())
            except Exception as e:
                Console.error(str(e))

    @staticmethod
    def edges(name, edges):
        db = FlowDatabase(name)
        for edge in edges:
            try:
                db.add_edge(edge[0], edge[1])
            except Exception as e:
                Console.error(str(e))


    @staticmethod
    def upload(classname):
        nodes = Get.nodes(classname)
        name = Get.name(classname)
        edges = Get.edges(classname)

        Put.nodes(name, nodes)
        Put.edges(name, edges)


parser = Lark(grammar, start = "expr")


class Flow():
    def __init__(self, arguments):

        self.flowfile = arguments[0]
        self.flowname = self.flowfile[:self.flowfile.find("-flow")]

        if len(arguments) == 1:
            self._upload()
        if len(arguments) == 2:
            self.node = arguments[1]
            self._run(self.node)

    def _save(self, task_name, result):
        """
        saves the results to the database into the task with the name provided.
        :param task_name: The name of the task
        :type task_name: string
        :param result: The dict of the result
        :type result: dict
        :return: None
        :rtype: None
        """
        print("saving result to", self.flowname, result)
        db = FlowDatabase(self.flowname, True)
        db.add_node_result(task_name, result)


    def _run(self, task_name):
        """
        execute the python method in the class with the given task_name
        :param task_name: the name of the task
        :type task_name: string
        :return: the dict after the execution of the task
        :rtype: dict
        """
        method = None
        for (name, func) in inspect.getmembers(self):
            if name == task_name:
                method = func
        result = method()
        self._save(task_name, result)
        return result

    def _upload(self):
        Put.upload(self.__class__)

class FlowDatabase(object):

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
        # find all modified

        # return self.collection.find(query)
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
    db = FlowDatabase(flowname)
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
    db = FlowDatabase()
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
