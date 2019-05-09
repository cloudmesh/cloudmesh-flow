from flask import Flask, jsonify, render_template, render_template_string
from flask import jsonify
import oyaml as yaml
from os import walk
from cloudmesh.flow.worflowdb import WorkFlowDB

class Node:

    @staticmethod
    def color(task):
        color = 'violet'
        if task.status == "pending":
            color = 'lightblue'
        elif task.status == "running":
            color = 'orange'
        elif task.status == "error":
            color = 'red'
        elif task.status == "finished":
            color = 'green'
        return color

    @staticmethod
    def properties(d):
        d['label'] = d['id']
        if d['id'] in ['start']:
            d['shape'] =  'diamond'
            d['color']= 'yellow'
        elif d['id'] in ['end']:
            d['color']= 'grey'
            d['shape'] =  'diamond'
        else:
            d['shape'] = 'box'
            d['widthConstraint'] = 100
        d['font.size'] = '24'
        d['font.color'] = 'black'
        d['font.face'] = 'arial'
        d['value'] = 2
        d['shadow'] = True
        return d

    @staticmethod
    def start_end():
        nodes = [
            Node.properties({'id': 'start', 'x': 0, 'y': 0}),
            Node.properties({'id': 'end', 'x': 300})]
        return nodes

def get_workflow_names():
    workflows = []
    mydb = WorkFlowDB()
    flows = mydb.list_all_workflows()
    for flow in flows:
        workflow = {"name" : flow, "modified" : ""}
        workflows.append(workflow)

    return jsonify(workflows)





def refresh(workflowname):
    workflowname = workflowname[:-5]
    mydb = WorkFlowDB(workflowname)
    tasks = mydb.list_nodes()

    nodes = Node.start_end()
    edges = []


    to_end_nodes = [x.name for x in tasks]

    for task in tasks:
        nodes.append(Node.properties({'id': task.name,
                      'color': Node.color(task),
                      "modified" : task.modified ,
                      "dependencies" : task.dependencies,
                      "progress" : task.progress,
                      "done" : task.done}))
        if len(task.dependencies) == 0:
            edges.append({'from': 'start', 'to': task.name, "arrows": 'to', 'width': 2})
        for dependency in task.dependencies:
            edges.append({'from': dependency, 'to': task.name, "arrows": 'to', 'width': 2})
            to_end_nodes.remove(dependency)

    for end in to_end_nodes:
        edges.append({'from': end, 'to': 'end', "arrows": 'to', 'width': 2})

    flow = []
    flow.append({"nodes" : nodes, "edges" : edges})

    return jsonify(flow)

def show(workflowname):
    workflowname = workflowname[:-5]
    mydb = WorkFlowDB(workflowname)
    tasks = mydb.list_nodes()

    nodes = Node.start_end()
    edges = []

    to_end_nodes = [x.name for x in tasks]

    for task in tasks:
        nodes.append(Node.properties({'id': task.name, 'color': Node.color(task)}))
        if len(task.dependencies) == 0:
            edges.append({'from': 'start', 'to': task.name, "arrows": 'to', 'width': 2})
        for dependency in task.dependencies:
            edges.append({'from': dependency, 'to': task.name, "arrows": 'to', 'width': 2})
            to_end_nodes.remove(dependency)

    for end in to_end_nodes:
        edges.append({'from': end, 'to': 'end', "arrows": 'to', 'width': 2})

    return render_template("workflow.html", nodes=nodes, edges=edges)

def showFromDirectory(workflowname):
    filename = "workflows/" + workflowname + ".yaml"
    with open(filename, "r") as stream:
        data = yaml.load(stream, Loader=yaml.SafeLoader)

    tasks = data["tasks"]
    for task in tasks:
        print(task)

    nodes = Node.start_end()
    edges = []

    for task in tasks:
        nodes.append(Node.properties({'id': task}))

    flows = data["flow"].split("|")
    for flow in flows:
        arrows = flow.split(";")

        for i in range(0, len(arrows) - 1):
            edges.append({'from': arrows[i], 'to': arrows[i + 1], "arrows": 'to', 'width': 2})

    return render_template("workflow.html", nodes=nodes, edges=edges)


def update(workflow):
    flow = workflow.get("flowyaml", None)
    workflowname = workflow.get("name", None)
    filename = "workflows/" + workflowname + ".yaml"
    data = yaml.load(flow, Loader=yaml.SafeLoader)
    with open(filename, 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False)
    show(workflowname)

def getworkflownamesFromDirectory():
    workflows = []
    for (dirpath, dirnames, filenames) in walk("workflows"):
        for filename in filenames:
            if filename.endswith(".yaml"):
                flow = {"name" : filename[:-5]}
                workflows.append(flow)

    return jsonify(workflows)


