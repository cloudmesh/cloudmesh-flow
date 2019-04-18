from __future__ import print_function
from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from cloudmesh.flow.WorkFlow import WorkFlow, WorkFlowDB
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
                flow node add NODE NODENAME
                flow edge add FROM TO FLOWNAME

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
              --name    specify the name of the workflow (otherwise default is workflow)
              --log     specify the log file
              --flowname=FLOWNAME   the name or the workflow

        """

        arguments.FLOWNAME = arguments["--flowname"] or "workflow"
        VERBOSE(arguments)

        if arguments.add and arguments.NODE:

            node = Node(arguments.NODENAME)
            node.workflow = arguments.FLOWNAME
            db = WorkFlowDB(arguments.FLOWNAME)
            db.add_node(node.to_dict())

        elif arguments.list:

            db = WorkFlowDB(arguments.FLOWNAME)
            nodes = db.list_nodes()
            for node in nodes:
                print(node)

        elif arguments.edge and arguments.add:

            db = WorkFlowDB(arguments.FLOWNAME)
            db.add_edge(arguments.FROM, arguments.TO)

