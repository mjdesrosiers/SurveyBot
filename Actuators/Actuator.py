# -*- coding: utf-8 -*-
import Queue
from time import sleep
from threading import Thread, Event
import Command_Packet

class Actuator(object):

    def __init__(self, master_queue, get_timeout=0.5):
        self.cmd_queue = master_queue
        self.to_be_added = []
        self.worker_thread = None
        self.get_timeout = get_timeout

    def start(self):
        if self.worker_thread is None:
            self.stop_flag = Event()
            self.thd = Thread(target=self.data_action_loop, args=(self.act_on_cmd, self.stop_flag), name=self.__str__())
            self.thd.daemon = True
            self.thd.start()

    def data_action_loop(self, cmd_method, stop):
        while not stop.isSet():
            try:
                if not self.cmd_queue.empty():
                    cmd = self.cmd_queue.get(block=True, timeout=self.get_timeout)
                    if cmd is not None:
                        self.act_on_cmd(cmd)
                    else:
                        print("timeout on cmd get")
            except Exception as e:
                print("Exception found from {}: {}".format(self, e))
        print("stopping execution on {}".format(self))
        try:
            self.cleanup()
        except:
            print("error in cleanup")

    def stop(self):
        print("setting stop flag")
        self.stop_flag.set()


class TestActuator(Actuator):

    def __init__(self, master_queue, get_timeout=0.5):
        super(TestActuator, self).__init__(master_queue, get_timeout=get_timeout)

    def act_on_cmd(self, cmd):
        print("received command: {}".format(cmd))

    def cleanup(self):
        print("dummy interface cleaning up. should release all resources, close connections here")

    def __str__(self):
        return "<Test actuator w/ delay of {}>".format(self.get_timeout)

    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":
    from time import time
    import random
    print("starting!")
    mq1 = Queue.Queue()
    ta = TestActuator(mq1, get_timeout=0.01)
    ta.start()
    items_put = 0
    start = time()
    while items_put < 10:
        sleep(random.randint(1, 5))
        curr_time = time() - start
        mq1.put(Command_Packet.Command_Packet("<__main__>", curr_time))
        items_put += 1
    ta.stop()
    ta.thd.join()