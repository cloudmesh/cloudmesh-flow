from cloudmesh.flow.WorkFlow import WorkFlowDB
import subprocess
import time

class WorkflowRunner(object):
    def __init__(self, flowname):
        self.flowname = flowname
        self.db = WorkFlowDB(flowname)
        self.running_jobs = []

    def start_available_nodes(self):
        available_nodes = self.db.find_root_nodes()
        for node in available_nodes:
            print("starting a new node", node)
            self.start_node(node)
        
    def start_flow(self):
        self.running = True
        self.start_available_nodes()
        while(self.running):
            self.check_on_running_processes()
            self.running = len(self.running_jobs) > 0

    def start_node(self, node):
        self.db.set_node_status(node.name, "running")
        print("running command", node.get_command())
        process = subprocess.Popen(node.get_command())
        self.running_jobs.append({"handle" : process, "node" : node})

    def resolve_node(self, node, status):
        resolution = "finished" if status == 0 else "error"
        self.db.set_node_status(node.name, resolution)
        if status == 0:
            self.db.resolve_node_dependencies(node)


    def check_on_running_processes(self):
        for process in self.running_jobs:
            process_handle = process["handle"]
            status = process_handle.poll()
            if not status:
                continue
            else:
                self.resolve_node(process["node"], status)
        self.start_available_nodes()
        time.sleep(3)


if __name__ == "__main__":
    runner = WorkflowRunner("flow")
    runner.start_flow()
