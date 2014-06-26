'''
Created on 2013-5-31

@author: Zibo
'''

from tkinter import *
#from queue import Queue,Empty
from com.comx import Com
from com.txthread import TxThread

from gui.choices import Choices
from gui.multilistbox import MultiListbox

import time

class SendWin(Frame):
    '''
    classdocs
    '''


    def __init__(self,master=None,*cnf,**kws):
        '''
        Constructor
        '''
        Frame.__init__(self,master,*cnf,**kws)
        
        framechoices=Frame(master,*cnf,**kws)
        framechoices.pack(side=TOP,expand=YES,fill=X)
        
        #framedecision=Frame(master,*cnf,**kws)
        #framedecision.pack(side=TOP,expand=YES,fill=X)
        
        self.showChoices(framechoices)
        #self.showDecision(framedecision)

        
    def showChoices(self,master):            
        self.choices=Choices(master)
        self.choices.pack(expand=YES,fill=X)
                            
    def showDecision(self,master):
        #entry=Entry(master)
        #entry.pack(side=LEFT,fill=X,expand=YES)
        
        button=Button(master,
               text='Go!',
               command=lambda : print(repr(self.choices.get()))
               )
        button.pack(side=LEFT,expand=YES,fill=X)

               
if __name__ == '__main__':
    root=Tk()
  
    #sendframe=Frame()
    #sendframe.pack(side=TOP,expand=YES,fill=X)
    
    sendwin=SendWin(root)
    sendwin.pack()    
    #entry=Entry(frameEntry)
    #entry.pack(expand=YES,fill=X,side=TOP) 
    #root.protocol("WM_DELETE_WINDOW", sendwin.com.quit())       
    root.mainloop()