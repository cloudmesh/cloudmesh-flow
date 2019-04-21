# Workflow Management

This is a tool for managing workflows in a cloudmesh context. A
*workflow* is a set of Python functions (that we call tasks or nodes)
that need to be run together, some in sequence and some in
parallel. This tool allows you to define workflows, indicate how they
should be run, and run them. You can also visualize your workflows,
including the current status of nodes that are running, and the
dependency network between them.

## Getting Started

To use this tool, you'll need to already have cloudmesh
installed. Follow the instructions at the cloudmesh repository located
here. This tool relies on MongoDB within the cloudmesh command, so
you'll need to have Mongo up and running on your local machine.

To install this tool within cloudmesh, clone this repository and run 

```bash
pip install -e .
```

The commands then should be available by calling the flow commands via
cms. You can test that the installation went well by calling

```bash
cms flow list
```

to list your current tasks. The command should complete correctly but
output nothing.

### Adding Tasks

There are several ways to add tasks to your workflow. The simplest is
just to call `cms flow add $taskname`. For example, to add a task
named `a` call `cms flow add a`. This creates a reference to the task
in the database, and adds the task to your default workflow, which is
named `workflow`

By default, all tasks are run in parallel. Typically, you'll have
multiple tasks that you need to run, some in sequence some in
parallel. To add tasks `a`, `b`, and `c`, where `a` and `b` can be run
in parallel but `c` depends on `a`, execute the following sequence:

```bash
cms flow node add a
cms flow node add b
cms flow node add c
cms flow add edge c a
```

This creates the 3 above nodes, and then adds the dependency. You can
check that the nodes were added successfully by running

```bash
cms flow list
```
Your output should look similar to this:

```commandline
> cms flow list
Node "a" dependecies []
Node "b" dependencies []
Node "c" dependencies ["a"]

```

#### Multiple Workflows

Many times a user wants to have several different workflows
defined. You can manage several workflows by passing the `--flowname`
parameter to the `cms flow command`. For example, to add a new node in
the workflow `workflow2`, run

```bash
cms flow add node d --flowname=workflow2
```


Now you will have 2 workflows, the default one with the nodes we added
earlier, and the flow `workflow2`. You can see the different results
by running the list command on each

```bash
cms flow list
cms flow list --flowname=workflow2
```

### Adding A Complete Flow

While this process works for smaller workflows, it can be tedious to
add 10 or 15 tasks via the command line. You can add a flow by
defining a *flowstring*, which specifies many tasks and their
dependencies all at once.

A flowstring is a single string with a list of tasks, separated by
either a semicolon (;) or a double pipe (||). The semicolon indicates
sequential dependency and the pipe indicates parallel. A sample
flowstring for the flow we defined above is

`"a;c||b"`

Node `a` is joined sequentially with node `c` and in parallel with
node `b`.

#### Adding a Flow String

#### Adding a Flow YAML Definition

## Visualizing

The package `cloudmesh.flow.visualize` visualizes the workflows that
have been created by the `cloudmesh.flow` package.  This package
consists of a rest s ervice which essentially provides the following
two methods:

* `/list` method which lists the names of all the workflows
* `/monitor/{workflowname}` method which visualized the workflow named
  by `{workflowname}`

### Start the visualization service

To start the visualization service run the following command:

```bash
cms flow visualize
```
The visualization service will then be available at the address 

<http://127.0.0.1:8080/flow/

Here you can find the list of all the submitted workflows. By
selecting a workflow you can view a visualization of the workflow.

A node in a visualization has a color. The color represents the status
of the task associated with the node. If the task is pending for
execution, its color will be `blue` otherwise the color is `green`.

> ADD A SCREENSHOT AND PUT THE IMAGE IN an images/ dir


## Refernces

* This work is influenced by <https://github.com/cloudmesh/workflow>
