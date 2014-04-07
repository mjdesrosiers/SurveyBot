# -*- coding: utf-8 -*-
from Actuators import Motor_Controller, Command_Packet
import Queue
import time

if __name__ == "__main__":
    q = Queue.Queue()
    mc = Motor_Controller.Motor_Controller(q)
    mc.start()
    q.put(Command_Packet.Command_Packet("<__main__@stop_motors>", {Motor_Controller.CHANNEL_0: 0, Motor_Controller.CHANNEL_1: 0}))
    time.sleep(5)
    mc.stop()
    mc.thd.join()