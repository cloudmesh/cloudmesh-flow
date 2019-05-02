from cloudmesh.flow.WorkFlow import WorkFlowDB
from cloudmesh.flow.Node import Node
from cloudmesh.flow.visualize import manager


def define_flow():
    FLOWNAME = "testflow2"
    mydb = WorkFlowDB(FLOWNAME)
    node = Node("d")
    node.workflow = FLOWNAME

    mydb.add_node(node.toDict())

    node = Node("e")
    node.workflow = FLOWNAME

    mydb.add_node(node.toDict())

    node = Node("f")
    node.workflow = FLOWNAME

    mydb.add_node(node.toDict())

    node = Node("g")
    node.workflow = FLOWNAME

    mydb.add_node(node.toDict())

    node = Node("h")
    node.workflow = FLOWNAME

    mydb.add_node(node.toDict())

    mydb.add_edge("d", "e")
    mydb.add_edge("e", "f")
    mydb.add_edge("g", "h")



def list_flow(flow_name):
    flow_name = flow_name[:-5]
    mydb = WorkFlowDB(flow_name)
    tasks = mydb.list_nodes()
    for node in tasks:
        print(node.name)
        print(node.status)
        for dependency in node.dependencies:
            print(dependency)


    nodes = []
    edges = []

    nodes.append({'id': 'start', 'label': 'start'})
    nodes.append({'id': 'end', 'label': 'end'})

    to_end_nodes = [x.name for x in tasks]

    for task in tasks:
        nodes.append({'id': task.name, 'label': task.name})
        if len(task.dependencies) == 0:
            edges.append({'from': 'start', 'to': task.name, "arrows": 'to'})
        for dependency in task.dependencies:
            edges.append({'from': dependency, 'to': task.name, "arrows": 'to'})
            to_end_nodes.remove(dependency)

    for end in to_end_nodes:
        edges.append({'from': end, 'to': 'end', "arrows": 'to'})

    for edge in edges:
        print(edge["from"] , " -> " , edge["to"])
def list_flows():
    mydb = WorkFlowDB()
    all_workflows = mydb.list_all_workflows()
    for workflow in all_workflows:
        print(workflow)


list_flow("testflow2-flow")

manager.start()


