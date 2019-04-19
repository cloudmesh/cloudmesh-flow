from __future__ import print_function
from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from cloudmesh.flow.WorkFlow import  WorkFlowDB
from cloudmesh.DEBUG import VERBOSE
from cloudmesh.flow.Node import Node

class FlowCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_flow(self, args, arguments):
        """
        ::
          Usage:
                flow list [--flowname=FLOWNAME]
                flow add [--flowname=FLOWNAME] --flowfile=FILENAME
                flow run [--flowname=FLOWNAME]
                flow run --flowfile=FILENAME
                flow node add NODENAME
                flow edge add FROM TO [--flowname=] FLOWNAME

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
        VERBOSE(arguments)
        print("greetings!!!", arguments)
        if arguments.NODEAME and arguments.add:
            node = Node(arguments.NODENAME)
            node.workflow = arguments.FLOWNAME
            print("adding a node", node)
            db = WorkFlowDB(arguments.FLOWNAME)
            db.add_node(node.to_dict())
        elif arguments.list:
            print("listing nodes!")
            db = WorkFlowDB(arguments.FLOWNAME)
            print(db.collection)
            nodes = db.list_nodes()
            for node in nodes:
                print(node)
        elif arguments.edge and arguments.add:
            db = WorkFlowDB(arguments.FLOWNAME)
            db.add_edge(arguments.FROM, arguments.TO)


