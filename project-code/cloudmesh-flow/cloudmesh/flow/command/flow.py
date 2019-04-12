from __future__ import print_function
from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from cloudmesh.flow.api.manager import Manager
from cloudmesh.flow.WorkFlow import WorkFlow, WorkflowDB


class FlowCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_flow(self, args, arguments):
        """
        ::

          Usage:
                flow list
                flow add [--name=NAME] --file=FILENAME
                flow run [--name=NAME] [--log=LOG]
                flow run --file=FILENAME [--log=LOG]
                flow node add NODENAME NAME
                flow edge add FROM TO NAME

          This command manages and executes workflows

          Arguments:
              NAME       the name of the workflow
              FILENAME   a file name
              NODENAME   the name of the node
              FROM       the edge source
              TO         the edge destinationi

          Options:
              -f      specify the file

        """

        print(arguments)

        m = Manager()
        db = WorkflowDb()
        if arguments.NODE and arguments.add:
            node = arguments.NODENAME
            add_node(node)
            print(node)
        elif arguments.list:
            print("option b")
            m.list("just calling list without parameter")

        def add_node(node):
            print("adding a node", node)
            new_node = Node(node)
            db.add_node(node)
             

        def add_dep(node1, node2):
            db.add_edge(node1, node2)

        def parse_flow_string(string):
            flow = Workflow("workflow", string)

        def generate_flow_string():
            pass
