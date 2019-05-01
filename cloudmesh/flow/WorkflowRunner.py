from cloudmesh.flow.WorkFlow import WorkFlowDB
import subprocess
import time
import json


class WorkflowRunner(object):
    def __init__(self, flowname, filename = None):
        self.flowname = flowname
        self.db = WorkFlowDB(flowname)
        self.running_jobs = []
        self.filename = filename or f"{flowname}-flow.py"

    def start_available_nodes(self):
        available_nodes = self.db.find_root_nodes()
        for node in available_nodes:
            print("starting a new node", node)
            self.start_node(node)
        
    def start_flow(self):
        self.running = True
        self.db.start_flow()
        self.start_available_nodes()
        while(self.running):
            self.check_on_running_processes()
            self.running = len(self.running_jobs) > 0

    def start_node(self, node):
        self.db.set_node_status(node.name, "running")
        print("running command", node.get_command())
        process = subprocess.Popen(node.get_command(), stdout=subprocess.PIPE )
        self.running_jobs.append({"handle" : process, "node" : node})

    def resolve_node(self, node, status, output = {}):
        resolution = "finished" if status == 0 else "error"
        self.db.set_node_status(node.name, resolution)
        self.db.add_node_result(node.name, output)
        if status == 0:
            self.db.resolve_node_dependencies(node)


    def check_on_running_processes(self):
        for process in self.running_jobs:
            process_handle = process["handle"]
            status = process_handle.poll()
            if status is None:
                continue
            else:
                printed_output = process_handle.communicate()[0]
                print(printed_output)
                output = json.loads(printed_output)
                self.resolve_node(process["node"], status, output)
        self.start_available_nodes()
        time.sleep(3)


if __name__ == "__main__":
    runner = WorkflowRunner("flow")
    runner.start_flow()
