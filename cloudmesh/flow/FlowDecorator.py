import inspect
from cloudmesh.flow.WorkFlow import WorkFlowDB

class BaseWorkFlow():
    def __init__(self, flowfile):
        self.flowname = flowfile[:flowfile.find("-")]

    def save_result_to_db(self, nodeName, result):
        print("saving result to", self.flowname, result)
        db = WorkFlowDB(self.flowname, True)
        db.add_node_result(nodeName, result)


    def runCommand(self, commandName):
        method = None
        for (name, func) in inspect.getmembers(self):
            if name == commandName:
                method = func
        result = method()
        self.save_result_to_db(commandName, result)
        return result




