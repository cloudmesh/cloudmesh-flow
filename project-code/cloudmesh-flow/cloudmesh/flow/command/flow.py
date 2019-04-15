from __future__ import print_function
from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from cloudmesh.flow.api.manager import Manager
from cloudmesh.flow.WorkFlow import WorkFlow, WorkFlowDB


class FlowCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_flow(self, args, arguments):
        """
        ::

          Usage:
                flow list [--flowname=NAME]
                flow add [--flowname=NAME] --flowfile=FILENAME
                flow run [--flowname=NAME]
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

          Options:
              --file    specify the file
              --name    specify the name of the workflow (otherwise default is workflow)
              --log     specify the log file

        """

        print("greetings!!!", arguments)
        DEFAULT_FLOW = "workflow"
        if arguments.NODE and arguments.add:
            node = Node(arguments.NODENAME)
            flow = DEFAULT_FLOW
            if arguments.NAME:
                flow = arguments.NAME
            node.workflow = flow
            db = WorkFlowDB(flow)
            db.add_node(node.to_dict())
        elif arguments.list:
            flow = DEFAULT_FLOW
            if arguments.NAME:
                flow = arguments.NAME
            db = WorkFlowDB(flow)
            nodes = db.list_nodes()
            for node in nodes:
                print(node)
        elif arguments.edge and arguments.add:
            source = arguments.FROM
            dest = arguments.TO
            flow = DEFAULT_FLOW
            if arguments.NAME:
                flow = arguments.NAME
            db = WorkFlowDB(flow)
            db.add_edge(source, dest)

