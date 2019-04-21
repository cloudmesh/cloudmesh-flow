from __future__ import print_function
from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from cloudmesh.flow.WorkFlow import  WorkFlowDB, parse_string_to_workflow, parse_yaml_to_workflow
from cloudmesh.flow.WorkflowRunner import WorkflowRunner
from cloudmesh.DEBUG import VERBOSE
from cloudmesh.flow.Node import Node
from cloudmesh.common.console import Console

class FlowCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_flow(self, args, arguments):
        """
        ::
          Usage:
                flow list [--flowname=FLOWNAME]
                flow add [--flowname=FLOWNAME] --flowfile=FILENAME
                flow run [--flowname=FLOWNAME] [--flowfile=FILENAME]
                flow node add NODENAME [--flowname=FLOWNAME]
                flow edge add FROM TO [--flowname=FLOWNAME]
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
        """

        arguments.FLOWNAME = arguments["--flowname"] or "workflow"
        arguments.FLOWFILE = arguments["--flowfile"] or f"{arguments.FLOWNAME}-flow.py"
        VERBOSE(arguments)
        print("greetings!!!", arguments)

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

            print("listing nodes!")
            db = WorkFlowDB(arguments.FLOWNAME)
            print(db.collection)
            nodes = db.list_nodes()
            for node in nodes:
                print(node)

        elif arguments.run:

            runner = WorkflowRunner(arguments.FLOWNAME, arguments.FLOWFILE)
            runner.start_flow()

        elif arguments.visualize:

            Console.error("not implemented")


