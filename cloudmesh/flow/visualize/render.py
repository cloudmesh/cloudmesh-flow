from flask import Flask, jsonify, render_template, render_template_string
from flask import jsonify
import oyaml as yaml
from os import walk
from cloudmesh.flow.worflowdb import WorkFlowDB


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

    nodes = []
    edges = []

    nodes.append({'id': 'start', 'label': 'start', 'color' : 'yellow', 'x' : 40, 'y' : 200})
    nodes.append({'id': 'end', 'label': 'end', 'color' : 'indigo', 'font': {'color':'white'}})

    to_end_nodes = [x.name for x in tasks]

    for task in tasks:
        color = 'green'
        if task.status == "pending":
            color = 'lightblue'
        nodes.append({'id': task.name, 'label': task.name, 'color': color, "modified" : task.modified , "dependencies" : task.dependencies, "progress" : task.progress, "done" : task.done})
        if len(task.dependencies) == 0:
            edges.append({'from': 'start', 'to': task.name, "arrows": 'to'})
        for dependency in task.dependencies:
            edges.append({'from': dependency, 'to': task.name, "arrows": 'to'})
            to_end_nodes.remove(dependency)

    for end in to_end_nodes:
        edges.append({'from': end, 'to': 'end', "arrows": 'to'})

    flow = []
    flow.append({"nodes" : nodes, "edges" : edges})

    return jsonify(flow)

def show(workflowname):
    workflowname = workflowname[:-5]
    mydb = WorkFlowDB(workflowname)
    tasks = mydb.list_nodes()

    nodes = []
    edges = []

    nodes.append({'id': 'start', 'label': 'start', 'color' : 'yellow', 'x': 132, 'y': 286})
    nodes.append({'id': 'end', 'label': 'end', 'color' : 'indigo', 'font': {'color':'white'}})

    to_end_nodes = [x.name for x in tasks]

    for task in tasks:
        color = 'violet'
        if task.status == "pending":
            color = 'lightblue'
        elif task.status == "running":
            color = 'orange'
        elif task.status == "error":
            color = 'red'
        elif task.status == "finished":
            color = 'green'
        nodes.append({'id': task.name, 'label': task.name, 'color': color})
        if len(task.dependencies) == 0:
            edges.append({'from': 'start', 'to': task.name, "arrows": 'to'})
        for dependency in task.dependencies:
            edges.append({'from': dependency, 'to': task.name, "arrows": 'to'})
            to_end_nodes.remove(dependency)

    for end in to_end_nodes:
        edges.append({'from': end, 'to': 'end', "arrows": 'to'})

    return render_template("workflow.html", nodes=nodes, edges=edges)

def showFromDirectory(workflowname):
    filename = "workflows/" + workflowname + ".yaml"
    with open(filename, "r") as stream:
        data = yaml.load(stream)

    tasks = data["tasks"]
    for task in tasks:
        print(task)

    nodes = []
    edges = []

    for task in tasks:
        nodes.append({'id': task, 'label': task})

    nodes.append({'id': 'start', 'label': 'start'})
    nodes.append({'id': 'end', 'label': 'end'})

    flows = data["flow"].split("|")
    for flow in flows:
        arrows = flow.split(";")

        for i in range(0, len(arrows) - 1):
            edges.append({'from': arrows[i], 'to': arrows[i + 1], "arrows": 'to'})

    return render_template("workflow.html", nodes=nodes, edges=edges)


def update(workflow):
    flow = workflow.get("flowyaml", None)
    workflowname = workflow.get("name", None)
    filename = "workflows/" + workflowname + ".yaml"
    data = yaml.load(flow)
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


