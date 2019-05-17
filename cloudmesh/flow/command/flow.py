from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from cloudmesh.flow.Flow import  FlowDatabase, parse_yaml_to_workflow
from cloudmesh.flow.FlowRunner import FlowRunner
from cloudmesh.common.debug import VERBOSE
from cloudmesh.flow.Node import Node
from cloudmesh.common.Printer import Printer
from cloudmesh.mongo.CmDatabase import CmDatabase
from cloudmesh.flow.visualize import manager


class FlowCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_flow(self, args, arguments):
        """
        ::
          Usage:
                flow list [--flow=NAME] [--output=FORMAT]
                flow add [--flowname=FLOWNAME] --flowfile=FILENAME
                flow run [--flowname=FLOWNAME] [--flowfile=FILENAME]
                flow node add NODENAME [--flowname=FLOWNAME]
                flow edge add FROM TO [--flowname=FLOWNAME]
                flow node delete NODENAME
                flow edge delete FROM TO
                flow edge invert FROM TO
                flow visualize start
                flow visualize stop
                flow refresh

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
              --flow=NAME   the name or the flow
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

            db = FlowDatabase(arguments.FLOWNAME)
            db.add_edge(arguments.FROM, arguments.TO)

        elif arguments["add"]:

            print("adding a node")

            if arguments.NODENAME:

                node = Node(arguments.NODENAME)
                node.workflow = arguments.FLOWNAME
                try:
                    db = FlowDatabase(arguments.FLOWNAME)
                    db.add_node(node.toDict())
                except Exception as e:
                    print ("error executing", e)

            elif arguments["--flowfile"]:

                filename = arguments["--flowfile"]
                print("load from file", filename)
                parse_yaml_to_workflow(filename)


        elif arguments["list"]:

            arguments.flow = arguments["--flow"] or "workflow"
            db = CmDatabase()



            name = arguments["--flow"]

            if name is not None:
                flows = [name]
            else:
                candidates = db.collections()
                flows = []
                for flow in candidates:
                    if flow.endswith("-flow"):
                        flows.append(flow)

            entries = []
            for name in flows:
                nodes = db.find(collection=f"{name}-flow")

                for node in nodes:
                    node["dependencies"] = ", ".join(node["dependencies"])
                entries = entries + nodes

            order = ["name", "workflow", "dependencies", "cm.modified"]
            header = ["Name", "Workflow", "Dependencies", "Modified"]


            print(Printer.flatwrite(nodes,
                                    order=order,
                                    header=header,
                                    output=arguments.output))






        elif arguments._run:

            runner = FlowRunner(arguments.FLOWNAME, arguments.FLOWFILE)
            runner.start_flow()

        elif arguments.visualize:

            if arguments["start"]:
                manager.start()
                print("The visualization servive started at http://127.0.0.1:8080/flow/")

            elif arguments["stop"]:
                manager.shutdown()

        elif arguments["delete"] and arguments.edge:
            db = FlowDatabase(arguments.FLOWNAME)
            db.remove_edge(arguments.FROM, arguments.TO)


        elif arguments["delete"] and arguments.node:
            db = FlowDatabase(arguments.FLOWNAME)
            db.remove_node(arguments.NODENAME)


        elif arguments["invert"] and arguments.edge:
            db = FlowDatabase(arguments.FLOWNAME)
            db.remove_edge(arguments.TO, arguments.FROM)
            db.add_edge(arguments.FROM, arguments.TO)

        elif arguments.refresh:

            raise NotImplementedError
            # shuld refresh the viz



