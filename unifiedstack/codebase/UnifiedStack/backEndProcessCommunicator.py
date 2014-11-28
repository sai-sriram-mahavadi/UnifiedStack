import zmq
import random
import sys
import time
from subprocess import Popen 
from logger.models import ConsoleLog

class FrontEndMessenger:    
    def __init__(self):
        self.port = "5556"
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PAIR)
        self.socket.bind("tcp://*:%s" % self.port)

    def start_recieving(self):
        while True: 
            msg = self.socket.recv()
	    ConsoleLog(console_summary=msg).save()
            print msg + " ==from BackEnd"
            time.sleep(10)

def startbackEndProcess():
    Popen(["python","integrator.py"])
    FrontEndMessenger().start_recieving()
    

if __name__=="__main__":
    startbackEndProcess() 
