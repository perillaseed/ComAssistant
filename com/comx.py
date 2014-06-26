'''
Created on 2013年9月4日

@author: Seed
'''
from tkinter import *
from serial import *
import time
from queue import Queue,Empty
from com.rxthread import RxThread
from com.txthread import TxThread
from com.updatethread import UpdateThread
from threading import Timer

import logging.config
from configparser import ConfigParser,RawConfigParser,SafeConfigParser
import re

import logging
#logging.basicConfig(format='%(levelname)s %(asctime)s %(module)s %(funcName)s %(lineno)d %(message)s', datefmt='%Y-%m-%d %H:%M:%S',level=logging.DEBUG)
#logger=logging.getLogger(__name__)
logging.config.fileConfig('..\config\logging.ini',disable_existing_loggers=False)
logger = logging.getLogger('xlogger')

from com.packager import Packager

class Com():
    '''
    classdocs
    '''
    def __init__(self,port,file='..\config\packager.ini',packerstyle='default',**cnf):
        '''
        Constructor
        '''
        self.default=Com.getini()        
        dict(self.default,**cnf)
        #print(default)
        logger.debug(self.default)
        
        self.ser=Serial(**self.default)
        self.ser.port=port.upper()        
        self.txqueue=Queue()
        self.rxqueue=Queue()
        self.outputqueue=Queue()
        
        self.recvthread=None
        self.sendthread=None
        self.outputthread=None
        self.packer=Packager(file,packerstyle)
        
        self.outputs=None
        #self.startrx()
        #self.starttx()

    @classmethod
    def getList(cls):
        """scan for available ports. return a list of tuples (num, name)"""
        available = []
        for i in range(256):
            try:
                s = Serial(i)
                available.append((i, s.portstr))
                s.close()    # explicit close 'cause of delayed GC in java
            except SerialException:
                pass
        #print(available)
        logger.debug(available)
        return available
    
    @staticmethod
    def checkCom(portname):
        #print(list(map(lambda port:port[1],self.getList())))
        logger.debug(list(map(lambda port:port[1],Com.getList())))
        return portname in map(lambda port:port[1], Com.getList())
    
    @classmethod
    def openCom(cls,port,**cnf):
        #print(cnf)
        logger.debug(cnf)
        default=Com.getini()        
        dict(default,**cnf)
        #print(default)
        logger.debug(default)
        try:
            com = Serial(port, **default)
            if com.isOpen():
                return com
            else:
                com.open()
                return com
        except SerialException as e:
            #print(e)
            logger.error(e)
            return None
    @classmethod
    def closeCom(cls,com):
        try:
            com.close()
        except Exception as e:
            #print(e)
            logger.error(e)   
    @classmethod
    def getini(cls,file='..\config\com.ini',section='default'):
        config=ConfigParser()
        config.SECTCRE = re.compile(r"\[ *(?P<header>[^]]+?) *\]")
        config.optionxform = lambda option: option
        config.read(file)  
        #p=re.compile(r'\s*,\s*')
        comparas=dict(config.items(section,raw=True))    
        for k in comparas:
            comparas[k]=eval(comparas[k])
        #print(comparas)
        #logger.debug(comparas)
        return comparas
    
    def setini(self,file='..\config\history.ini'):
        config=RawConfigParser()
        config.read(file)
        
        with open(file, 'w') as configfile:
            config[self.port]=self.default
            #config.update()
            config.write(configfile, space_around_delimiters=False)
    
    def send(self,data):
        #print('write: ', data.decode('ascii'))
        logger.debug(data)
        self.txqueue.put(data)        
        
    def recv(self):
        while self.rxqueue.qsize():
            try:
                data=self.rxqueue.get()
                if data:                
                    #print('read: '+data.decode('ascii'))
                    logger.debug(data)
                    self.outputqueue.put(data) 
                    return data
                else:
                    pass
            except Empty:
                pass                   

    def outputto(self,outputs):
        self.outputs=outputs
                        
            
    def update(self,name='update'):
        #print(packer.styles)
        #print(packer.sections)
        #print(packer.style)
        while self.outputqueue.qsize():
            try:
                data=self.outputqueue.get()
                logger.debug(data)
                if data: 
                    if self.outputs!=None:               
                        for output in self.outputs:
                            try:                               
                                #for unpacked in self.packer.unpack(data):
                                #    output.insert(END,' '+unpacked)
                                unpacked=self.packer.unpack(data)
                                output.insert(END,unpacked) 
                                output.insert(END,unpacked[-1])                                                                  
                                output.yview(END)                                
                            except Exception as e:
                                sys.stdout.write('Output to %s failed' %output)
                                sys.stdout.write('\n' + str(e)+'\n')
                                pass                    
                    else:                        
                        sys.stdout.write(data['data'])
                        sys.stdout.write('\n')
                        sys.stdout.flush()
                        pass                                      
                else:
                    #return 'break'
                    pass
            except Empty:
                return 'break'
                pass
        #Timer(0.5, self.update,outputs).start()

    def close(self):
        try:
            #self.ser.flushoutputs()
            #self.ser.flushInput()
            #self.ser.flush()
            self.stoptx()            
            self.stoprx()
            self.stopupdate()
            self.flushtx()
            self.flushrx()
            self.flushoutput()          
            self.ser.close()            
        except Exception as e:
            #print(e)
            logger.error(e)
        
    def isOpen(self):
        try:
            return self.ser.isOpen()
        except Exception as e:
            #print(e)
            logger.error(e)
    
    def open(self):
        try:
            self.ser.open()
        except Exception as e:
            #print(e)
            logger.error(e)
            
    def startrx(self,name='Rx'):
        if not self.recvthread:
            self.recvthread = RxThread(self,name)
            self.recvthread.daemon=True
            self.recvthread.start()
            #print('new:',self.recvthread)
            logger.info('new:' + repr(self.recvthread))
        #print('old:',self.recvthread)
        logger.info('old:' + repr(self.recvthread))
        
    def starttx(self,name='Tx'):
        if not self.sendthread:
            self.sendthread=TxThread(self,name)
            self.sendthread.daemon=True
            self.sendthread.start()
            #print('new:',self.sendthread)
            logger.info('new:' + repr(self.sendthread))
        #print('old:',self.sendthread)
        logger.info('old:' + repr(self.sendthread))
        
    def startupdate(self,func=None,name='update'):
        if func is None:
            func=self.update
        if not self.outputthread:
            self.outputthread=UpdateThread(self,func,name)
            self.outputthread.daemon=True
            self.outputthread.start()
            #print('new:',self.outputthread)
            logger.info('new:' + repr(self.outputthread))
        #print('old:',self.outputthread)
        logger.info('old:' + repr(self.outputthread))
        
    def stoprx(self):
        if self.recvthread is not None:
            if self.recvthread.is_alive():
                try:
                    self.recvthread.kill()
                    #print('killed: ', self.recvthread)
                    logger.info('killed:' + repr(self.recvthread))
                    self.recvthread=None
                    self.flushrx()
                except Exception as e:
                    #print('Stop rx Failed')
                    logger.error('Stop rx Failed')
                    #print(e)
                    logger.error(e)
                    return 'break'
            
    def stoptx(self):
        if self.sendthread is not None:
            if self.sendthread.is_alive():
                try:
                    self.sendthread.kill()
                    #print('killed: ', self.sendthread)
                    logger.info('killed:' + repr(self.sendthread))
                    self.sendthread=None
                    self.flushtx()
                except Exception as e:
                    #print('Stop tx Failed')
                    logger.error('Stop tx Failed')
                    #print(e)
                    logger.error(e)
                    return 'break'
                
    def stopupdate(self):
        if self.outputthread is not None:
            if self.outputthread.is_alive():
                try:
                    self.outputthread.kill()
                    #print('killed: ', self.outputthread)
                    logger.info('killed:' + repr(self.outputthread))
                    self.outputthread=None
                    self.flushoutput()
                except Exception as e:
                    #print('Stop update Failed')
                    logger.error('Stop update Failed')
                    #print(e)
                    logger.error(e)
                    return 'break'
    def flushtx(self):
        with self.txqueue.mutex:
            self.txqueue.queue.clear()
            
    def flushrx(self):
        with self.rxqueue.mutex:
            self.rxqueue.queue.clear()
            
    def flushoutput(self):
        with self.outputqueue.mutex:
            self.outputqueue.queue.clear()
    
    def echo(self,outputs=None):
        self.startrx()
        self.starttx()
        self.startupdate()
        #self.update() here need to couple with Timer(0.01,self.update,outputs)
        #self.update()        
        while True:
            #self.update here need to forbid the Timer(0.01,self.update,outputs)
            #self.update()
            #com.read()
            data=self.recv()
            if data:                    
                print(data)
                logger.debug(self.packer.unpack(data))
                self.send(data['data'].encode('ascii'))
                #time.sleep(0.1)
            time.sleep(0.5)
            
            
class Demo(Frame):
    def __init__(self,master,*cnf,**kws):
        Frame.__init__(self,master,*cnf,**kws)
        
        self.showRecv(master,*cnf,**kws)      
        
        self.choice=StringVar()
        
        coms=Com.getList()
        
        if coms is not None:
            framechoice=Frame(master)
            framechoice.pack(expand=YES,fill=BOTH)
            for num,name in coms:
                self.text.insert(END, '%d %s' %(num,name) + '\n')
                radiobutton=Radiobutton(framechoice,text=name,value=name,variable=self.choice)
                radiobutton.pack(side=LEFT,expand=YES,fill=X)
                radiobutton.config(command=lambda : logger.info(self.choice.get()))
        
        button=Button(master,text='read')
        button.bind('<Button-1>',lambda event : self.toggleupdate(event,'basic'))
        button.pack(expand=YES,fill=X)

        
        Button(master,text='write',command=self.send).pack(side=BOTTOM,expand=YES,fill=X)
                
        self.entry=Entry(master)
        self.entry.pack(side=BOTTOM,expand=YES,fill=X)
        
        Button(master,text='open',command=self.openCom).pack(side=LEFT,expand=YES,fill=X)
        
        Button(master,text='startrx',command=self.startrx).pack(side=LEFT,expand=YES,fill=X)
        
        Button(master,text='starttx',command=self.starttx).pack(side=LEFT,expand=YES,fill=X)
        
        Button(master,text='stoprx',command=self.stoprx).pack(side=LEFT,expand=YES,fill=X)
        
        Button(master,text='stoptx',command=self.stoptx).pack(side=LEFT,expand=YES,fill=X)
        
        Button(master,text='close',command=self.close).pack(side=LEFT,expand=YES,fill=X)
        
        
          
    def showRecv(self,master,*cnf,**kws):
        frame=Frame(master,*cnf,**kws)
        frame.pack(expand=YES,fill=BOTH) 
        self.text=Text(frame)
        scrollbar=Scrollbar(frame,command=self.text.yview())
        self.text.configure(yscrollcommand=scrollbar.set)        
        self.text.pack(side=LEFT,expand=YES,fill=BOTH)
        scrollbar.pack(side=RIGHT,expand=NO,fill=Y)    
        
    def openCom(self):
        self.com=Com(self.choice.get())
        self.com.outputto([self.text,])
    
    def startrx(self):
        self.com.startrx()
        
    def starttx(self):
        self.com.starttx()
        
    def stoptx(self):
        self.com.stoptx()
        
    def stoprx(self):
        self.com.stoprx()
        
    def close(self):
        try:
            self.com.close()
            #sys.exit()
        except Exception as e:
            #print(e)
            logger.error(e)
            sys.exit()
     
    def toggleupdate(self,event,name='Update'):
        if self.com.outputthread is not None:
            if self.com.outputthread.is_alive():
                self.com.stopupdate()
            event.widget.config(bg='RED')
        else:
            #self.com.outputto(self.text)
            self.com.startupdate(self.recv,name)
            event.widget.config(bg='GREEN')
      
    def send(self):
        data=self.entry.get().encode('ascii')
        self.com.send(data)
        self.entry.delete(0, END)
    '''    
    def recv(self,outputs):
        self.com.recv()
        self.com.update(outputs)
        self.after(10, self.recv,outputs)
    '''
    def recv(self,name='update'):
        self.com.recv()
        self.com.update(name)
                   
            
if __name__=='__main__':      
    #logging.config.fileConfig(r'./../config/logging.ini',disable_existing_loggers=False)    
    #logger=logging.getLogger('rflogger')
    #logger.info(data)
    #logger.info(com.ser.isOpen())
    
    '''
    for x in Com.getList():
        print(x)   
   
    com=Com('Com1')
    com.echo()
    '''   
    #com.close()
    #logging.shutdown()
    #'''
    
    
    root=Tk()
    
    demo=Demo(root)
    demo.pack()    
    root.bind('<Return>',lambda e : demo.send())
    
    root.mainloop()
    #'''