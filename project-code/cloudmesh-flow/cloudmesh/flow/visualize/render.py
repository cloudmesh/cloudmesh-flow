from flask import Flask, jsonify, render_template, render_template_string
from flask import jsonify
import oyaml as yaml
from os import walk



def show(workflowname):
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

def getworkflownames():
    workflows = []
    for (dirpath, dirnames, filenames) in walk("workflows"):
        for filename in filenames:
            if filename.endswith(".yaml"):
                flow = {"name" : filename[:-5]}
                workflows.append(flow)

    return jsonify(workflows)


