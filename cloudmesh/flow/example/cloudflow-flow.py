from cloudmesh.compute.Provider import Provider
from cloudmesh.flow.FlowDecorator import BaseWorkFlow

#
# we assume image is ubuntu 19.04 in cloudmesh4.yaml
#
def start_vm(cloud, name=None):
    #
    # complete me
    #
    provider = Provider(cloud)
    vm = provider.boot(name=name)
    vm.wiat()
    return vm
    
    

class MyFlow(BaseWorkFlow):
    
        
    def start_aws(self):
        vm = start_vm("aws", name="aws01")
        
    def start_azure(self):
        vm = start_vm("azure", name="aazure01")
        r = vm.ssh("uname -a")

    def ping_aws(self):
        provider = Provider("aws")
        provider.ping(name="aws01")

    def ping_azure(self):
        provider = Provider("azure")
        provider.ping(name="azure01")
        
    def ssh_azure(self):
        provider = Provider("azure")
        r = provider.ssh(name="azure01")
        
    def ssh_aws(self):
        provider = Provider("aws")
        r = provider.ssh(name="aws01")
        

if __name__ == "__main__":
    Flow = MyFlow(sys.argv[0])
    Flow.runCommand(sys.argv[1])

    # please specify workflow here
    
    """
    start -> start_aws -> ping_aws -> ssh_aws -> end
    start -> start_azure -> ping_azure -> ssh_aws -> end
    """
    
    
