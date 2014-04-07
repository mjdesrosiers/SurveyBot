class Data_Packet(object):

    def __init__(self, originator, data):
        self.originator = originator
        self.data = data

    def __str__(self):
        return "Data from <{}>: {}".format(str(self.originator), str(self.data))

