Workflow Management
=============

This is a tool for managing workflows in a cloudmesh context. A _workflow_ is a set of Python functions (that we call tasks or nodes) that need to be run together, some in sequence and some in parallel. This tool allows you to define workflows, indicate how they should be run, and run them. You can also visualize your workflows, including the current status of nodes that are running, and the dependency network between them.

## Getting Started
To use this tool, you'll need to already have cloudmesh installed. Follow the instructions at the cloudmesh repository located here. This tool relies on MongoDB within the cloudmesh command, so you'll need to have Mongo up and running on your local machine.

To install this tool within cloudmesh, clone this repository and run `pip install -e .` The commands then should be available by calling the flow commands via cms. You can test that the installation went well by calling `cms flow list` to list your current tasks. The command should complete correctly but output nothing.

### Adding Tasks
There are several ways to add tasks to your workflow. The simplest is just to call `cms flow add $taskname`. For example, to add a task named "a" call `cms flow add a`. This creates a reference to the task in the database, and adds the task to your default workflow, which is named "workflow"

By default, all tasks are run in parallel. Typically, you'll have multiple tasks that you need to run, some in sequence some in parallel. To add tasks "a", "b", and "c", where "a" and "b" can be run in parallel but "c" depends on "a", execute the following sequence:
```bash
cms flow node add a
cms flow node add b
cms flow node add c
cms flow add edge c a
```

This creates the 3 above nodes, and then adds the dependency. You can check that the nodes were added successfully by running `cms flow list`. You output should look similar to this:
```commandline
> cms flow list
Node "a" dependecies []
Node "b" dependencies []
Node "c" dependencies ["a"]

```
#### Multiple Workflows
Many times a user wants to have several different workflows defined. 

### Adding A Complete Flow

#### Adding a Flow String

#### Adding a Flow YAML Definition

## Visualizing
