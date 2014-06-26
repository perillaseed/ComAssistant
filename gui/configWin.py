import sys
from tkinter import *
from tkinter.simpledialog import messagebox
from com.comx import Com
from configparser import ConfigParser
import serial
import time
import threading
from queue import Queue,Empty

import logging
#logging.basicConfig(format='%(levelname)s %(asctime)s %(module)s %(funcName)s %(lineno)d %(message)s', datefmt='%Y-%m-%d %H:%M:%S',level=logging.DEBUG)
#logger=logging.getLogger(__name__)
logging.config.fileConfig('..\config\logging.ini',disable_existing_loggers=False)
logger = logging.getLogger('xlogger')

class ConfigWin(Frame):
    def __init__(self,master=None,coms=Com.getList(),file='..\config\com.ini', **kws):
        Frame.__init__(self, master, kws)
        '''
        try:
            ConfWin.append((Com.getList()[-1:][0][0]+1,'Fresh'))
        except Exception as e:
            print(e)
        '''        
        self.showOpts(file,master,**kws)
        self.coms=coms
        self.com=None
        
        self.frameConfWin=Frame(master,**kws)
        self.frameConfWin.pack(expand=YES,fill=X)
        
        self.outputs=None
        
        #self.showComs(master,coms,**kws)
        
        self.setOpts()           
        #self.variables={}    
        
    def showComs(self,master,coms,**kws):        
        for tab in coms:
            #print(tab)
            #logger.debug(tab)            
            #Button(text=tab[1],command=lambda tabname=tab[1]: sys.stdout.write(tabname+'\n')).grid(row=0,column=tab[0],sticky=W)
            button=Button(self.frameConfWin,
                   text=tab[1],
                   bg='GREEN'
                   #command=lambda tabname=tab[1]: self.connectCom(tabname)
                   )
            button.bind('<Button-1>',
                        self.togglecom
                        #lambda event: self.connectCom(event.widget['text'])
                        )
            button.pack(side=LEFT,fill=X,expand=YES)
            
        Button(self.frameConfWin,
                   text='Refresh',
                   command=lambda :self.refresh(master)
                   ).pack(side=LEFT,fill=X,expand=YES)
                   
    def refresh(self,master):
        self.frameConfWin.destroy()
        self.showComs(Com.getList(), master)
        
    
    def showOpts(self,file,master,**kws):
        frameOpts=Frame(master,**kws)
        frameOpts.pack(expand=YES,fill=X)           
        config=ConfigParser()
        config.SECTCRE = re.compile(r"\[ *(?P<header>[^]]+?) *\]")
        config.optionxform = lambda option: option
        config.read(file)
        config.remove_section('default')
        self.variables={}
        parameters=dict(
                       map(
                           lambda m:[m,dict(config.items(m))],
                           config.sections()
                           )
                       )
        for k in sorted(parameters):
            self.variables[k]=StringVar(master)
            Label(frameOpts, 
                  text=k                  
                  ).pack(side=LEFT,fill=X,expand=YES)
            OptionMenu(frameOpts, 
                       self.variables[k],
                       *sorted(parameters[k].keys())
                       ).pack(side=LEFT,fill=X,expand=YES)
                       
    def getOpts(self,port):
        return dict(
                   map(lambda m: (m,self.variables[m].get()),
                       self.variables.keys()
                       )
                   )
    
    def setOpts(self,**kws):
        for k in self.variables:
            self.variables[k].set(dict(Com.getini(),**kws)[k])                
                    
    def openCom(self,event):
        if self.outputs is None:
            self.outputs=Text(self.frameConfWin)
        self.outputs.pack(side=TOP,expand=YES,fill=BOTH)
        widget=event.widget
        try:
            self.com=Com(widget['text'],**self.getOpts(widget['text']))
            if not self.com.isOpen():
                self.com.open()
            self.com.outputto([self.outputs,])                
            self.com.startrx()
            self.com.starttx()
            self.com.startupdate(self.recv)           

            widget.config(bg='RED')
            return self.com
        except Exception as e:
            #print(e)
            logger.error(e)
            return 'break'
        
    def closeCom(self,event):
        self.com.close()
        event.widget.config(bg='GREEN')
            
    def togglecom(self,event):
        widget=event.widget
        if widget['bg']=='GREEN':
            self.openCom(event)
        else:
            self.closeCom(event)      

    def recv(self):
        self.com.recv()
        self.update()     
        
    def send(self,widget):
        if self.com is not None:
            if self.com.isOpen():
                data=widget.get().encode('ascii')
                self.com.send(data)
                widget.delete(0,END)
            else:
                messagebox.showinfo('出错啦！', '串口被关了吧？')
        else:
            messagebox.showinfo('出错啦！', '忘了开串口吧？')
        
    def toggleupdate(self,func,event):
        widget=event.widget
        if self.com.outputthread is not None:
            if self.com.outputthread.is_alive():
                self.com.stopupdate()
                widget.config(bg='GREEN')
                
        else:
            self.com.startupdate(self.recv)
            widget.config(bg='RED')
    
    def startupdate(self):
        self.com.startupdate(self.recv)
        
    def stopupdate(self):
        self.com.stopupdate()
        
    def update(self,name='update'):

        #print(packer.styles)
        #print(packer.sections)
        #print(packer.style)
        while self.com.outputqueue.qsize():
            try:
                data=self.com.outputqueue.get()
                logger.debug(data)
                if data: 
                    if self.com.outputs!=None:             
                        for output in self.com.outputs:
                            try:
                                i=0                                
                                #unpacked='\t'.join(self.packer.unpack(data))
                                if 'Rx' in self.com.packer.unpack(data):
                                    colors=['RED','YELLOW']
                                    bgcolor='GRAY'
                                elif 'Tx' in self.com.packer.unpack(data):
                                    colors=['BLUE','RED']
                                    bgcolor='WHITE'                                
                                for unpacked in self.com.packer.unpack(data):
                                    i=i+1
                                    fgcolor=colors[i%2]
                                    #bgcolor=colors[1-i%2]
                                    output.insert(END,' '+unpacked)
                                    end_index = output.index('end')
                                    begin_index = "%s-%sc" % (end_index, len(unpacked)+2)                        
                                    output.tag_add('tag'+data['time']+str(i), begin_index, end_index)
                                    output.tag_config('tag'+data['time']+str(i), foreground=fgcolor, background=bgcolor)
                                output.tag_config('tag'+data['time']+str(i), foreground='BLACK', background='WHITE')
                                
                                output.yview(END)
                                
                            except Exception as e:
                                sys.stdout.write('Output to %s failed' %output)
                                sys.stdout.write('\n')
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
           
            
if __name__=='__main__':
    root=Tk()
    frameConfWin=Frame(root)
    frameConfWin.pack(side=TOP,expand=YES,fill=X)
       
    configwin=ConfigWin(master=frameConfWin,coms=Com.getList())
    configwin.pack(side=TOP,expand=YES,fill=X)
    
    #text=Text(root)
    
    for tab in Com.getList():
        button=Button(frameConfWin,
               text=tab[1],
               bg='GREEN'
               )
        button.bind('<Button-1>',
                    lambda event : configwin.togglecom(event)
                    )
        
        button.pack(side=LEFT,fill=X,expand=YES)
    

    

    entry=Entry(root)
    entry.pack(side=LEFT,expand=YES,fill=X)

    buttonsend=Button(root,text='send!',command=lambda : configwin.send(entry))
    buttonsend.pack(side=LEFT,expand=YES,fill=X)    
  
    root.bind('<Return>', lambda e : configwin.send(entry))  
    
    root.mainloop()