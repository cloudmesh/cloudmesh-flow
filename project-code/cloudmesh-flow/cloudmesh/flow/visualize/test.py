import js2py


import oyaml as yaml
import requests
from flask import jsonify
import json
import os

workflows = []
for (dirpath, dirnames, filenames) in os.walk("workflows"):
    for filename in filenames:
        if filename.endswith(".yaml"):
            flow = {"name": filename}
            workflows.append(flow)



with open("sampleflow1.yaml", "r") as stream:
    data = yaml.load(stream)

tasks = data["tasks"]
for task in tasks:
    print(task)

nodes = []
edges = []

for task in tasks:
    nodes.append({'id': task, 'label': task})

nodes.append({'id':'start', 'lable':'start'})
nodes.append({'id':'end', 'lable':'end'})

flows = data["flow"].split("|")
for flow in flows:
    arrows = flow.split(";")

    for i in range(0, len(arrows) - 1):
        edges.append({'from':arrows[i], 'to': arrows[i+1], "arrows":'to'})


url = "http://127.0.0.1:8080/flow/monitor"
response = requests.get(url)

flow = json.dumps(data)

flowyaml = {"flowyaml" : flow}

workflow = json.dumps(flowyaml)

response = requests.post(url, json=flowyaml)

print(response.content)

def visualize(workflow):
    flows = workflow.split("|")







