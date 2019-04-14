class Node(object):
    def __init__(self, name):
        self.name = name
        self.dependencies = []
        self.workflow = ""

    def add_dependency(self, other_node):
        self.dependencies.append(other_node.name)

    def toDict(self):
        return {"name": self.name, "dependencies": self.dependencies,
                "workflow": self.workflow}

    def workflow_filename(self):
        return f"flow-{self.workflow}.py"
    
    def get_command(self):
        return ["python", self.workflow_filename(), self.name]

    def __repr__(self):
        return self.name
