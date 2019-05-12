import sys
import time
from cloudmesh.flow.Flow import Flow
from cloudmesh.flow.Flow import Get, Put

from pprint import pprint

class MyFlow(Flow):

    edges = [["a","b"], ["b","c"]]

    def a(self):
        print("in a!")
        time.sleep(5)

    def b(self):
        print("in b!")
        time.sleep(10)

    def c(self):
        print("in c!")
        time.sleep(10)

if __name__ == "__main__":
    # argv[0] : the name of the workflow
    # argv[1] : a node to be executed
    # if only the first argument is provided the workflow will be uploaded to mongo
    flow = MyFlow(sys.argv)
