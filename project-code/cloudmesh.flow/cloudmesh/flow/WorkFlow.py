#!/usr/bin/python
import sys
import re
from cloudmesh.mongo.CmDatabase import CmDatabase
from cloudmesh.flow.Node import Node

SPLIT_CHARS = ["\|", "&", ";"]
SPLIT_RE = re.compile("|".join(SPLIT_CHARS))


class WorkFlow:
    def __init__(self, name, flowstring):
        self.flowstring = flowstring
        nodes = SPLIT_RE.split(flowstring)
        flow_nodes = []
        self.database = CmDatabase()
        self.name = name
        for node in nodes:
            flow_node = Node(node)
            flow_node.workflow = name
            print(flow_node)
            flow_nodes.append(flow_node)
            self.database.insert(flow_node.toDict())

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
    flowstring = sys.argv[1]
    flow = WorkFlow("myflow", flowstring)
    print(flow)
    flow.run()
