import serial
from queue import Queue,Empty
from tkinter import *
from com.kthread import KThread
import time
from threading import Timer
from com.packager import Packager

class UpdateThread(KThread):
    def __init__(self,com,func,name='Update', *args,**kws):
        KThread.__init__(self,*args,**kws)
        self.com=com
        self.com.flushoutput()
        self.setName(name)
        if func is None:
            self.func=self.com.update
        else:
            self.func=func
        
    def run(self):
        #ser = serial.Serial('COM1',9600)
        while True:
            self.func()
            time.sleep(0.001)

        
            
            
        
