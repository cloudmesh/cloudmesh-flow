class Node():
    def __init__(self, name):
        self.name = name
        self.dependencies = []
        self.workflow = ""

    def add_dependency(self, other_node):
        self.dependencies.append(other_node.name)
    
    def toDict(self):
        return {"name": self.name, "dependencies" : self.dependencies, "workflow" : self.workflow}

    def __repr__(self):
       return self.name

