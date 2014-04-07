# -*- coding: utf-8 -*-
from Actuator import Actuator
import Motor_Controller
import Queue
import math as m
import Command_Packet

PROPORTIONAL_FACTOR = 4000  #LOLWUT

class Steering_Drive_Actuator(Actuator):

    def __init__(self, master_queue, track, get_timeout=0.05):
        super(Steering_Drive_Actuator, self).__init__(master_queue, get_timeout)
        self.mc_queue = Queue.Queue()
        self.mc = Motor_Controller.Motor_Controller(self.mc_queue)
        self.mc.start()
        self.track = track

    def act_on_cmd(self, cmd):
        gps_current = cmd.command['gps_point']
        otd = self.track.otd(gps_current)
        print("otd -> {}".format(otd))
        pkt = self.decide_mc_commands_from_otd(otd)
        self.mc_queue.put(pkt, block=True)

    def decide_mc_commands_from_otd(self, otd):
        #TODO make this actually work lulz
        motor0_val = Motor_Controller.FULL_FWD
        motor1_val = Motor_Controller.FULL_FWD
        if otd < 0:
            motor0_val -= int(abs(otd) * PROPORTIONAL_FACTOR)
        else:
            motor1_val -= int(abs(otd) * PROPORTIONAL_FACTOR)
        return Command_Packet.Command_Packet(self, {Motor_Controller.CHANNEL_0: motor0_val,
                                                    Motor_Controller.CHANNEL_1: motor1_val})

    def cleanup(self):
        print("Steering/Drive Actuator cleaning up")
        self.mc.cleanup()
        print("waiting for mc to finish")
        #self.mc.thd.join()
        print("motor controller finished closing")