from cloudmesh.compute.aws import Provider as AWSProvider
from cloudmesh.compute.azure import AzProvider
from cloudmesh.flow.FlowDecorator import BaseWorkFlow

class MyFlow(BaseWorkFlow):
    def spawn_aws(self):
        pass

    def spawn_azure(self):
        pass

    def ping_aws(self):
        pass

    def ping_azure(self):
        pass
    

if __name__ == "__main__":
    Flow = MyFlow(sys.argv[0])
    Flow.runCommand(sys.argv[1])
