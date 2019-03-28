#!/usr/bin/python
import sys
import re
from Node import Node

SPLIT_CHARS = ["\|", "&", ";"]
SPLIT_RE = re.compile("|".join(SPLIT_CHARS)) 


class WorkFlow:
    def __init__(self, name, flowstring):
        self.flowstring = flowstring
        nodes = SPLIT_RE.split(flowstring)
        flow_nodes = []
        self.name = name
        for node in nodes:
            flow_node = Node(node)
            flow_node.workflow = name 
            print(flow_node)
            flow_nodes.append(flow_node)
    def __repr__(self):
        return " ".join([self.name, self.flowstring])

    def run(self):
        pass

if __name__ == "__main__":
    flowstring = sys.argv[1]
    print(WorkFlow("myflow", flowstring))
