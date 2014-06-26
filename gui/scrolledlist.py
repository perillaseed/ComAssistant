import sys
from tkinter import *
from com.comx import Com
from configparser import ConfigParser
import serial
import time
import threading

CMD=[
       ('1 剪切', 'lambda e=e: e.widget.event_generate("<Control-x>")'),
       ('2 复制', 'lambda e=e: e.widget.event_generate("<Control-c>")'),
       ('3 粘贴', 'lambda e=e: e.widget.event_generate("<Control-v>")'),
       ]

class ScrolledList(Frame):
    '''
    classdocs
    '''
    def __init__(self, scrolleditems, master=None, cnf={}):
        '''
        Constructor
        '''
        Frame.__init__(self, master,cnf)
        self.pack(expand=YES,fill=BOTH)
        self.makeWidgets(scrolleditems)
        self.curselection=None
        
    def getSelectedItem(self,event):
        event.widget.selection_clear(0,END)
        self.index = event.widget.nearest(event.y)            
        self.curselection=self.listbox.get(self.index)
        
        #print(self.curselection)
        self.infoentry.delete(0,END)
        self.infoentry.insert(0,self.curselection)
        
        #不激活的话，初次运行，第一次左键，然后在另一项上右键，会出现下划线和选中颜色不是同一项的问题
        event.widget.activate(self.index)       
    
    def handleList(self,event):
        self.getSelectedItem(event)        
        self.runCommand(self.curselection)
    
    def runCommand(self,selection):
        print('You selected:',selection)    
        
    def showContext(self,event):
        #self.getSelectedItem(event)
        Context(event.widget,CMD[1:2],self.listbox)      
    
    def makeWidgets(self,options):        
        lbox=Listbox(self,relief=SUNKEN)

        xsbar=Scrollbar(self,orient=HORIZONTAL)
        ysbar=Scrollbar(self,orient=VERTICAL)
        
        lbox.config(xscrollcommand=xsbar.set,
                    yscrollcommand=ysbar.set,
                    selectmode = EXTENDED)
        xsbar.config(command=lbox.xview)
        ysbar.config(command=lbox.yview)
        
        
        
        ientry=Entry(self,bg='GREEN')
        
        ientry.pack(side=BOTTOM,expand=YES,fill=X)
        xsbar.pack(side=BOTTOM,fill=X)   
        ysbar.pack(side=RIGHT,fill=Y)
        lbox.pack(side=LEFT,expand=YES,fill=BOTH)       

     
        for label in options:
            lbox.insert(END,label)
                       
        lbox.config(selectmode=EXTENDED,setgrid=1)
        
        lbox.bind('<Button-1>',
                  self.getSelectedItem)
        lbox.bind('<Double-1>',
                  self.handleList)
        lbox.bind('<Button-3>',
                  lambda event:Context(event.widget,CMD[1:2],self.listbox))
        ientry.bind('<Button-3>',
                    lambda event:Context(event.widget,CMD,self.listbox))
        
        self.listbox=lbox
        self.infoentry=ientry
        
class Context(Menu):
    '''
    classdocs
    '''
    def __init__(self,bindTo,cmds,master=None,cnf={}):
        '''
        Constructor
        '''
        Menu.__init__(self,tearoff=0,master=None,cnf={})
        #for lbl,cmd in sorted(cmds.items()):
        #    self.add_command(label=lbl,command=cmd(self.event))
        self.cmds=cmds            
        bindTo.bind('<Button-3>',self.rClicker, add='')           
       
    def rClicker(self,e):
        ''' right click context menu for all Tk Entry and Text widgets
        '''        
        try:
            e.widget.focus()
    
            rmenu = Menu(None, tearoff=0, takefocus=0)
    
            for (txt, cmd) in self.cmds:
                rmenu.add_command(label=txt, command=eval(cmd))
    
            rmenu.tk_popup(e.x_root+40, e.y_root+10,entry="0")    
        except TclError:
            print(' - rClick menu, something wrong')
            pass    
        return "break"
    
    def rClickbinder(self,r):    
        try:
            for b in [ 'Text', 'Entry', 'Listbox', 'Label']: #
                r.bind_class(b, sequence='<Button-3>',
                             func=self.rClicker, add='')
        except TclError:
            print(' - rClickbinder, something wrong')
            pass  