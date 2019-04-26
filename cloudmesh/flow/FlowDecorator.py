import inspect
from abc import ABC


class BaseWorkFlow(ABC):
    
    def runCommand(self, commandName):
        method = inspect.getmembers(self).get(commandName)
        print(method)
        result = method()
        return result




