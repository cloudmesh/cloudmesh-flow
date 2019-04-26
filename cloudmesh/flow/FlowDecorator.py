import inspect

class BaseWorkFlow():
    def __init__(self, flowfile):
        self.flowname = flowfile[:flowfile.find("-")]

    def runCommand(self, commandName):
        method = None
        for (name, func) in inspect.getmembers(self):
            if name == commandName:
                method = func
        result = method()
        return result




