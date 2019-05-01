from __future__ import print_function
from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand, map_parameters
from cloudmesh.flow.WorkFlow import  WorkFlowDB, parse_string_to_workflow, parse_yaml_to_workflow
from cloudmesh.flow.WorkflowRunner import WorkflowRunner
from cloudmesh.DEBUG import VERBOSE
from cloudmesh.flow.Node import Node
from cloudmesh.common.console import Console
from cloudmesh.common.Printer import Printer
from pprint import pprint
from cloudmesh.mongo.CmDatabase import CmDatabase


class FlowCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_flow(self, args, arguments):
        """
        ::
          Usage:
                flow list [--flowname=FLOWNAME] [--output=FORMAT]
                flow add [--flowname=FLOWNAME] --flowfile=FILENAME
                flow run [--flowname=FLOWNAME] [--flowfile=FILENAME]
                flow node add NODENAME [--flowname=FLOWNAME]
                flow edge add FROM TO [--flowname=FLOWNAME]
                flow node delete NODENAME
                flow edge delete FROM TO
                flow edge invert FROM TO
                flow visualize

          This command manages and executes workflows
          The default workflow is just named "workflow" but you can specify multiple

          Arguments:
              NAME       the name of the workflow
              FILENAME   a file name
              NODENAME   the name of the node
              FROM       the edge source (a node name)
              TO         the edge destination (a node name)
              NODE       the name of the node

          Options:
              --file    specify the file
              --log     specify the log file
              --flowname=FLOWNAME   the name or the workflow
              --output=OUTPUT       the output format [default: table]
        """

        arguments.FLOWNAME = arguments["--flowname"] or "workflow"
        arguments.FLOWFILE = arguments["--flowfile"] or f"{arguments.FLOWNAME}-flow.py"
        arguments.output = arguments["--output"]


        VERBOSE(arguments, verbose=0)

        if arguments["add"] and arguments.edge:

            db = WorkFlowDB(arguments.FLOWNAME)
            db.add_edge(arguments.FROM, arguments.TO)

        elif arguments["add"]:

            print("adding a node")

            if arguments.NODENAME:

                node = Node(arguments.NODENAME)
                node.workflow = arguments.FLOWNAME
                try:
                    db = WorkFlowDB(arguments.FLOWNAME)
                    db.add_node(node.toDict())
                except Exception as e:
                    print ("error executing", e)

            elif arguments["--flowfile"]:

                filename = arguments["--flowfile"]
                print("load from file", filename)
                parse_yaml_to_workflow(filename, arguments.FLOWNAME)

        elif arguments["list"]:

            #print("listing nodes!")
            #db = WorkFlowDB(arguments.FLOWNAME)
            #print(db.collection)
            #nodes = db.list_nodes()
            #pprint (nodes)
            #for node in nodes:
            #    print(node)

            db = CmDatabase()
            nodes = db.find(collection=f"{arguments.FLOWNAME}-flow")

            order = ["name", "workflow", "dependencies", "cm.modified"]
            header = ["Name", "Workflow", "Dependencies", "Modified"]

            for node in nodes:
                node["dependencies"] = ", ".join(node["dependencies"])
            print(Printer.flatwrite(nodes,
                                    order=order,
                                    header=header,
                                    output=arguments.output))


        elif arguments.run:

            runner = WorkflowRunner(arguments.FLOWNAME, arguments.FLOWFILE)
            runner.start_flow()

        elif arguments.visualize:

            Console.error("vizulize not implemented")

        elif arguments["delete"] and arguments.edge:
            db = WorkFlowDB(arguments.FLOWNAME)
            db.remove_edge(arguments.FROM, arguments.TO)


        elif arguments["delete"] and arguments.node:
            db = WorkFlowDB(arguments.FLOWNAME)
            db.remove_node(arguments.NODENAME)


        elif arguments["invert"] and arguments.edge:
            db = WorkFlowDB(arguments.FLOWNAME)
            db.remove_edge(arguments.FROM, arguments.TO)
            db.add_edge(arguments.TO, arguments.FROM)



