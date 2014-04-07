# -*- coding: utf-8 -*-
import Queue
from time import sleep
from threading import Thread, Event
from Data_Packet import Data_Packet

class Sensor(object):

    def __init__(self, master_queue, delay=0.5):
        self.data_queue = master_queue
        self.to_be_added = []
        self.worker_thread = None
        self.delay = delay

    def start(self):
        if self.worker_thread is None:
            self.stop_flag = Event()
            self.thd = Thread(target=self.data_yield_loop, args=(self.data_source, self.stop_flag), name=self.__str__())
            self.thd.daemon = True
            self.thd.start()

    def data_yield_loop(self, data_method, stop):
        while not stop.isSet():
            #print("before method on " + str(self))
            data_point = data_method()
            #print("after method on " + str(self))
            try:
                pkt = Data_Packet(self, data_point)
                if data_point is not None:
                    self.data_queue.put(pkt, block=True, timeout=0.05)
                retry = None
                while len(self.to_be_added):
                    retry = self.to_be_added.pop()
                    try:
                        self.data_queue.put(retry, block=False)
                    except Exception:
                        self.to_be_added.append(retry)
                        break
                sleep(self.delay)
            except Exception:
                self.to_be_added.append(pkt)
        print("stopping execution on {}".format(self))
        self.cleanup()

    def stop(self):
        print("setting stop flag")
        self.stop_flag.set()


class TestSensor(Sensor):

    def __init__(self, master_queue, name, mi=0, ma=10, delay=0.5):
        self.mi = mi
        self.ma = ma
        self.name = name
        super(TestSensor, self).__init__(master_queue, delay=delay)

    def data_source(self):
        import random
        return self.name + " : " + str(random.randint(self.mi, self.ma))

    def cleanup(self):
        print("dummy interface cleaning up. should release all resources, close connections here")

    def __str__(self):
        return "<Test sensor w/ delay of {}>".format(self.delay)

    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":
    print("starting!")
    mq1 = Queue.Queue()
    mq2 = Queue.Queue()
    ts1 = TestSensor(mq1, name="1", mi=100, ma=110, delay=1)
    ts2 = TestSensor(mq2, name="2", mi=90, ma=99, delay=4)
    ts1.start()
    ts2.start()
    for i in range(100):
        if not mq1.empty():
            data_pt = mq1.get(block=True, timeout=0.5)
            print("\treceived data point1: {}".format(data_pt.data))
        if not mq2.empty():
            data_pt = mq2.get(block=True, timeout=0.5)
            print("\treceived data point2: {}".format(data_pt.data))
    ts1.stop()
    ts2.stop()
    ts1.thd.join()
    ts2.thd.join()