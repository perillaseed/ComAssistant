import serial
from queue import Queue,Empty
from tkinter import *
from com.kthread import KThread
import time
from threading import Timer
import threading

from com.packager import Packager
import binascii


import logging
#logging.basicConfig(format='%(levelname)s %(asctime)s %(module)s %(funcName)s %(lineno)d %(message)s', datefmt='%Y-%m-%d %H:%M:%S',level=logging.DEBUG)
#logger=logging.getLogger(__name__)
logging.config.fileConfig('..\config\logging.ini',disable_existing_loggers=False)
logger = logging.getLogger('xlogger')

class RxThread(KThread):
    def __init__(self, com, name='Rx',*args, **keywords):
        KThread.__init__(self,*args, **keywords)
        self.setName(name)
        self.com=com
        self.com.flushrx()
        self.packer=self.com.packer
        
        
    def run(self):
        #ser = serial.Serial('COM1',9600)
        while True:
            if not self.com.isOpen():
                self.com.open()            
            self.recv()
            time.sleep(0.001)
                
    def recv(self):
        try:
            gotdata=self.com.ser.inWaiting()
            if gotdata:
                data = self.com.ser.readline(gotdata)
                logger.debug(data)
                packed=self.packer.pack(data)
                logger.debug(packed)
                #print('rx thread: rx: '+data.decode('ascii'))
                
                
                #print('%s' %__name__)
                #print('%s' %self.getName())
                #print('%s' %self._name)                 
                #print('%s' %self.__repr__())
                #print(threading.current_thread().__repr__())
                self.com.rxqueue.put(packed)
                #self.com.recv()
                #self.com.outputqueue.put(b'rx: '+ data)
        except Exception as e:
            print('Fatal Error:')
            print(e)
            #return 'break'

        
            
            
        
