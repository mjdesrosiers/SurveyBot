

class Command_Packet(object):

    def __init__(self, originator, command):
        self.originator = originator
        self.command = command

    def __str__(self):
        return "Data from <{}>: {}".format(str(self.originator), str(self.command))