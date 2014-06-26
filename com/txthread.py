'''
Created on 2013年8月23日

@author: Seed
'''
import time
from com.kthread import KThread
from queue import Empty

import logging
#logging.config.fileConfig(r'./../config/logging.ini',disable_existing_loggers=False)    
#logger=logging.getLogger('rflogger')
#logging.basicConfig(format='%(levelname)s %(asctime)s %(module)s %(funcName)s %(lineno)d %(message)s', datefmt='%Y-%m-%d %H:%M:%S',level=logging.DEBUG)
#logger=logging.getLogger(__name__)
logging.config.fileConfig('..\config\logging.ini',disable_existing_loggers=False)
logger = logging.getLogger('xlogger')

class TxThread(KThread):
    '''
    classdocs
    '''
    def __init__(self,com,name='Tx', *args, **keywords):
        KThread.__init__(self, *args, **keywords)
        self.setName(name)
        self.com=com
        self.com.flushtx()
        self.packer=self.com.packer
        
    def run(self):     
        while True:
            self.write()
            time.sleep(0.001)     
            
    def write(self):
        while self.com.txqueue.qsize():            
            try:
                data=self.com.txqueue.get()                
                if data:
                    #print('tx thread: tx: '+data.decode('ascii'))
                    logger.debug(data)
                    if not self.com.isOpen():
                        self.com.open()
                    self.com.ser.write(data)
                    packed=self.packer.pack(data)
                    logger.debug(packed)
                    self.com.outputqueue.put(packed)
            except Empty:
                pass        
        #Timer(0.01,self.write).start()
    

        