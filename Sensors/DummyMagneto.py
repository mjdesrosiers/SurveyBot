# -*- coding: utf-8 -*-
from Sensor import Sensor
import Queue


class DummyMagneto(Sensor):

    def __init__(self, master_queue):
        super(DummyMagneto, self).__init__(master_queue)
        self.has_sent_value = False

    def data_source(self):
        if not self.has_sent_value:
            return 150
        else:
            return None

    def cleanup(self):
        pass

if __name__ == "__main__":
    mq = Queue.Queue()
    dm = DummyMagneto(mq)
    dm.start()
    has_received_value = False
    while not has_received_value:
        if not mq.empty():
            val = mq.get(block=True, timeout=0.5)
            print(val)
            has_received_value = True
    dm.stop()
    dm.thd.join()
