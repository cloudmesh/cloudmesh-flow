import sys
import time
from cloudmesh.flow.FlowDecorator import BaseWorkFlow
from cloudmesh.cloud

class MyFlow(BaseWorkFlow):
    def spawn_aws_box(self):
        time.sleep(10)
        return {"spawned" : true, cloud : "aws", "ip" : "192.28.72.3"}


    def spawn_azure_box(self):
        time.sleep(13)
        return {"spawned" : true, cloud : "azure", "ip" : "192.28.72.3"}

    def ping_aws_box(self):

        pass

    def ping_azure_box(self):
        pass

if __name__ == "__main__":
    Flow = MyFlow(sys.argv[0])
    Flow.runCommand(sys.argv[1])