'''
Created on 2013-5-31

@author: Zibo
'''

from gui.multilistbox import MultiListbox
from com.comx import Com
from gui.choices import Choices

from tkinter import *
from tkinter.simpledialog import messagebox
import time

from queue import Empty

import logging
#logging.basicConfig(format='%(levelname)s %(asctime)s %(module)s %(funcName)s %(lineno)d %(message)s', datefmt='%Y-%m-%d %H:%M:%S',level=logging.DEBUG)
#logger=logging.getLogger(__name__)
logging.config.fileConfig('..\config\logging.ini',disable_existing_loggers=False)
logger = logging.getLogger('xlogger')

class RecvWin(Frame):
    '''
    classdocs
    '''


    def __init__(self,master,configwin,coms=Com.getList(),*cnf,**kws):
        '''
        Constructor
        '''
        Frame.__init__(self,master,*cnf,**kws)
        
        
        
        #self.showoutputs(master,*cnf,**kws)
        self.showcoms(master,*cnf,**kws)    
        
        self.configwin=configwin
        self.coms=coms
        
        self.com=None
            
        
    def showoutputs(self,master,*cnf,**kws):        
        columns=[['No.', 10, 'number'],
                 ['Time', 24, 'time','seconds'],
                 ['Direction', 15,'All','Tx','Rx'],
                 ['Raw Data', 30,'String','Hex','Oct','Bin'],
                 ['Code Data',30,'String','Hex','Oct','Bin']]
        self.mlb = MultiListbox(master, columns)
        self.mlb.pack(expand=YES,fill=BOTH)
        return self.mlb
        
        
    def showcoms(self,master,*cnf,**kws):
        self.framecoms=Frame(master,*cnf,**kws)
        self.framecoms.pack(side=TOP,expand=YES,fill=X)        
        for tab in Com.getList():
            button=Button(self.framecoms,
                   text=tab[1],
                   bg='GREEN'
                   )
            button.bind('<Button-1>',
                        lambda event : self.togglecom(event,self.configwin)
                        )
            
            button.pack(side=LEFT,fill=X,expand=YES)
            
    def opencom(self,event,configwin):
        widget=event.widget            
        try:
            self.com=Com(widget['text'],**configwin.getOpts(widget['text']))
            if not self.com.isOpen():
                self.com.open()
                
            if self.configwin.outputs is None:
                self.configwin.outputs=[self.showoutputs(self.configwin.frameConfWin),]
            self.com.outputto(self.configwin.outputs) 
                           
            self.com.startrx()
            self.com.starttx()
            self.com.startupdate(self.recv)           

            widget.config(bg='RED')
            return self.com
        except Exception as e:
            #print(e)
            logger.error(e)
            return None
        
    def closeCom(self,event):
        self.com.close()
        event.widget.config(bg='GREEN')
            
    def togglecom(self,event,configwin,outputs=None):
        
        widget=event.widget
        if widget['bg']=='GREEN':
            self.opencom(event,configwin)
        else:
            self.closeCom(event)      

    def recv(self):
        self.com.recv()
        self.update()     
        
    def send(self,widget):
        data=widget.get().encode('ascii')
        if self.com is not None:
            if self.com.isOpen():
                self.com.send(data)
                widget.delete(0,END)
            else:
                messagebox.showinfo('出错啦！', '串口被关了吧？')
        else:
            messagebox.showwarning('出错啦！', '忘了开串口了吧！')
                    
        
    def insert(self,*data):
        self.mlb.insert(END, *data)
        
    def update(self,name='update'):
        while self.com.outputqueue.qsize():
            try:
                data=self.com.outputqueue.get()
                logger.debug(data)
                if data: 
                    if self.com.outputs!=None:               
                        for output in self.com.outputs:
                            unpacked=self.com.packer.unpack(data)[0:-1]
                            try:                                                                                                 
                                output.insert(END,unpacked)
                                if 'Rx' in unpacked:
                                    output.itemconfig(END,fg='BLUE')
                                else:
                                    output.itemconfig(END,fg='GREEN')                                                                                                    
                                output.yview(END)                                
                            except Exception as e:
                                sys.stdout.write('Output to %s failed' %output)
                                sys.stdout.write('\n' + str(e)+'\n')
                                pass                    
                    else:                        
                        sys.stdout.write(data['data'])
                        sys.stdout.flush()
                        pass                                      
                else:
                    #return 'break'
                    pass
            except Empty:
                return 'break'
                pass
          


if __name__ == '__main__':

    root=Tk()
    
    frameConfWin=Frame(root)
    frameConfWin.pack(side=TOP,expand=YES,fill=X)
    
    from gui.configWin import ConfigWin   
    configwin=ConfigWin(master=frameConfWin,coms=Com.getList())
    configwin.pack(side=TOP,expand=YES,fill=X)
  
    recvframe=Frame()
    recvframe.pack(side=TOP,expand=YES,fill=X)
    
    recvwin=RecvWin(recvframe,configwin)
    recvwin.pack()
        
    entry=Entry(root)
    entry.pack(expand=YES,fill=X,side=TOP)
    
    button=Button(root,text='Go!',command=lambda : recvwin.send(entry))
    button.pack(expand=YES,fill=X,side=TOP)
    
    root.bind('<Return>', lambda event: recvwin.send(entry))
       
    root.mainloop()