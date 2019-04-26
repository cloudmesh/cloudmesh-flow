import inspect

class BaseWorkFlow():
    def __init_(self, flowfile):
        self.flowname = flowfile[:flowfile.find("-")]

    def runCommand(self, commandName):
        method = inspect.getmembers(self).get(commandName)
        print(method)
        result = method()
        return result




