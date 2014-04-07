# -*- coding: utf-8 -*-
import socket
import json
from Sensor import Sensor, TestSensor
import Queue
import select


class Socket_Sensor(Sensor):

    def __init__(self, master_queue, port, delay=0, host=''):
        super(Socket_Sensor, self).__init__(master_queue, delay)
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(1)
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)
        self.conn = None
        self.addr = None

    def data_source(self):
        out = None
        try:
            if self.conn:
                out = self.acquire_data()
            else:
                self.get_connection()
        except Exception:
            out = None
        return out

    def acquire_data(self):
        out = None
        try:
            data = self.conn.recv(1024)
            #data = self.sockfile.readline()
            if data:
                try:
                    interpret = json.loads(data)
                    for k in interpret:
                        interpret[k] = float(interpret[k])
                    out = interpret
                except Exception as e:
                    print("couldn't understand json: {}".format(e))
                    print("raw json was: '{}'".format(data))
                    out = None
            if not data:
                self.conn = None
                self.addr = None
        except socket.error as se:
            if ("Errno 10035" in se.__str__()):
                pass
            else:
                print("socket error in acquire_data: {}".format(se))
        except Exception as e:
            print("Exception in acquire_data: {}".format(e))
            out = None
        return out

    def get_connection(self):
        print("searching for new connection")
        self.conn, self.addr = None, None
        read, write, error = select.select([self.sock], [], [], 1)
        if self.sock in read:
            self.conn, self.addr = self.sock.accept()
            self.sockfile = self.sock.makefile('r+b')
            print("accepted a new client @ <{}>".format(self.addr))

    def cleanup(self):
        print("releasing socket connection")
        self.sock.close()

if __name__ == "__main__":
    sq = Queue.Queue()
    tq = Queue.Queue()
    ss = Socket_Sensor(sq, port=50007)
    ts = TestSensor(tq, name="Test_Sensor0")
    ss.start()
    ts.start()
    sensors = [ss, ts]
    try:
        while True:
            if not sq.empty():
                print(sq.get(block=True, timeout=0.5).data)
            if not tq.empty():
                pass
                #print(tq.get(block=True, timeout=0.5).data)
    except KeyboardInterrupt:
        for sensor in sensors:
            sensor.stop()
        for sensor in sensors:
            sensor.thd.join()