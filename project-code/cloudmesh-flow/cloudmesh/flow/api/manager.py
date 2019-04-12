class Manager(object):
    def __init__(self):
        print("init {name}".format(name=self.__class__.__name__))

    def list(self, parameter):
        print("list", parameter)


'''
       list
       add [--name=NAME] --file=FILENAME
       run [--name=NAME] [--log=LOG]
       run --file=FILENAME [--log=LOG]
       node add NODENAME NAME
       edge add FROM TO NAME
'''
