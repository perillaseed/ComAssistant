from tkinter import *
from gui.configWin import ConfigWin
from gui.scrolledlist import ScrolledList,Context
from gui.choices import Choices
from com.comx import Com



CMD=[
       ('1 剪切', 'lambda e=e: e.widget.event_generate("<Control-x>")'),
       ('2 复制', 'lambda e=e: e.widget.event_generate("<Control-c>")'),
       ('3 粘贴', 'lambda e=e: e.widget.event_generate("<Control-v>")'),
       ]



if __name__=='__main__':
    root=Tk()
    frameConfigWin=Frame(root)
    frameConfigWin.pack(side=TOP,expand=YES,fill=X)
       
    ConfigWin=ConfigWin(Com.getList(),master=frameConfigWin)
    ConfigWin.pack(side=TOP,expand=YES,fill=X)  
  
 
    frameEntry=Frame()
    frameEntry.pack(side=TOP,expand=YES,fill=X)
    
    entry=Entry(frameEntry)
    entry.pack(expand=YES,fill=X,side=TOP)
    context=Context(entry,CMD,frameEntry)
    
    frameTerminal=Frame(root)
    frameTerminal.pack(expand=YES,fill=BOTH)    
    scrolleditems = (('测试选项 - %s' %x) for x in range(200))
    scrolledlist=ScrolledList(scrolleditems,frameTerminal)
    scrolledlist.pack(side=TOP,expand=YES,fill=BOTH)
    
    frameChoices=Frame(root)
    frameChoices.pack(side=TOP,expand=YES,fill=X)
       
    choices=Choices(master=frameChoices)
    choices.pack(side=TOP,expand=YES,fill=X) 
       
    root.mainloop()
    