class Node(object):
    def __init__(self, name):
        self.name = name
        self.dependencies = []
        self.workflow = ""
        self.result = {}

    def add_dependency(self, other_node):
        self.dependencies.append(other_node.name)

    def toDict(self):
        return {"name": self.name,
                "dependencies": self.dependencies,
                "workflow": self.workflow}

    def workflow_filename(self):
        return f"{self.workflow}-flow.py"
    
    def get_command(self, filename=None):
        if not filename:
            filename = self.workflow_filename()
        return ["python", filename, self.name]

    def __repr__(self):
        return f"Node name:{self.name} dependencies:{self.dependencies}"
