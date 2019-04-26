import sys
import time
from cloudmesh.flow.FlowDecorator import BaseWorkFlow,

@
class MyFlow(BaseWorkFlow):
    def a():
        print("in a!")
        time.sleep(5)
    def b():
        print("in b!")
        time.sleep(10)
    def c():
        print("in c!")
        time.sleep(10)

if __name__ == "__main__":
    Flow = MyFlow(sys.argv[0])
    Flow.runCommand(sys.argv[1])