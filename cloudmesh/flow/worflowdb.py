from cloudmesh.mongo.CmDatabase import CmDatabase
from cloudmesh.flow.Node import Node
from cloudmesh.mongo.DataBaseDecorator import DatabaseUpdate

class WorkFlowDB(object):

    def __init__(self, name="workflow"):
        self.database = CmDatabase()
        self.workflow_name = name
        self.collection = self.database.collection(f"{name}-flow")

    def attributes(self, name):
        data = {
            "cm": {
                "kind": "flow",
                "cloud": self.workflow_name,
                "name": name
            },
            "kind": "flow",
            "cloud": self.workflow_name,
            "name": name
        }
        return data

    @DatabaseUpdate()
    def add_node(self, node):
        name = node["name"]
        node.update(self.attributes(name))
        return node

    def add_edge(self, node, depends_on):
        self.collection.update_one(
            {"name": node},
            {"$push": {"dependencies": depends_on}})

    def _node_from_db(self, db_obj):
        reconstructed = Node(db_obj["name"])
        reconstructed.workflow = self.workflow_name
        reconstructed.dependencies = db_obj["dependencies"]
        reconstructed.status = db_obj.get("status", "pending")
        reconstructed.progress = ""
        reconstructed.modified = ""
        reconstructed.done = ""
        return reconstructed

    def get_node(self, name=None):
        return self._node_from_db(self.collection.find_one({"name": name}))

    def list(self, node=None, edge=None):
        query = {}
        if node:  query["name"] = node
        if edge: query["dependencies"] = edge
        return self.collection.find(query)

    def list_nodes(self):
        return [self._node_from_db(node) for node in self.list()]

    def list_edges(self):
        return self.collection.aggregate(
            [{"$unwind": "$dependencies"},
             {"$project": {"to": "$name", "from": "$dependencies"}}])

    def list_all_workflows(self):
        all_colls = self.database.collections()
        return [name for name in all_colls if "flow" in name and "active" not in name]

    def set_node_status(self, node, status):
        return self.collection.update_one(
            {"name": node}, {"$set": {"status": status}})

    def find_root_nodes(self):
        root_nodes = self.collection.find(
            {"dependencies.0": {"$exists": False}, "status": "pending"})
        return [self._node_from_db(node) for node in root_nodes]

    def switch_to_active_flow(self):
        started_collection = f"{self.workflow_name}-flow-active"
        self.collection = self.database.collection(started_collection)

    def resolve_node_dependency(self, name=None):
        return self.collection.update_many(
            {"dependencies": name}, {"$pull": {"dependencies": name}})

    def add_specification(self, spec):
        pass

    def start_flow(self):
        started_collection = f"{self.workflow_name}-flow-active"
        self.collection.aggregate([
            {"$project": {
                "dependencies": 1,
                "cm": 1,
                "kind": 1,
                "cloud": 1,
                "name": 1,
                "status": "pending"}},
            {"$out": started_collection}])
        self.switch_to_active_flow()

    def add_graph(self, yamlfile):
        pass

    def last_update(self, workflow=None):
        """
        This method returns the last modified value associated with a
        database update to a node.

        :param workflow: The name of the workflow
        :type workflow: string
        :return: The time of the last update
        :rtype: string
        """
        raise NotImplementedError
        t = "the time string"
        return t
