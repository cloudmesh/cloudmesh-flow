from __future__ import print_function
from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from cloudmesh.flow.api.manager import Manager

class FlowCommand(PluginCommand):
    

    # noinspection PyUnusedLocal
    @command
    def do_flow(self, args, arguments):
        """
        ::

          Usage:
                workflow list
                workflow run FILENAME
                workflow node add NODENAME
                workflow edge add FROM TO

          This command does some useful things.

          Arguments:
              FILENAME   a file name
              NODENAME   the name of the node
              FROM       the edge source
              TO         the edge destinationi

          Options:
              -f      specify the file

        """

        print(arguments)

        m = Manager()


        if arguments.NODE and arguments.add:
            node = arguments.NODENAME
            add_node(node)
            print(node)
        elif arguments.list:
            print("option b")
            m.list("just calling list without parameter")


        def add_node(node):
            pass

        def add_dep(node1, node2):
            pass

        def parse_flow_string(string):
            pass

        def generate_flow_string():
            pass


