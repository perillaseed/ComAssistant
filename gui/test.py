'''
Created on 2013年8月9日

@author: Seed
'''
from tkinter import *
from configparser import ConfigParser
import re


        
def test():
    frame=Frame(root)
    frame.pack()
       
    button=Button(frame,text='hide',bg='yellow')
    button2=Button(frame,text='hide',bg='green')
    widget=Frame(root)
    widget.pack()
    label=Label(text='label')
    label.pack(in_=widget)
    label2=Label(text='label2')
    label2.pack(in_=widget)
    
    #button.bind(switchWidget(button,widget))
    button.config(command=lambda :switchWidgetWithAdjust(button,widget))
    button2.config(command=lambda :switchWidgetWithoutAdjust(button2,widget))
    
    button.pack(side=LEFT)
    button2.pack(side=LEFT)

def switchWidgetWithAdjust(switch,widget):
    if switch['text']=='show':
        widget.pack()
        switch['text']='hide'
    else:
        widget.pack_forget()
        switch['text']='show'
        
def switchWidgetWithoutAdjust(switch,widget):
    if switch['text']=='show':
        widget.lower()        
        switch['text']='hide'
    else:
        widget.lift()        
        switch['text']='show'
    

if __name__ == '__main__':
    root=Tk()
    #root.wm_attributes("-topmost", 0)    
    #root.wm_attributes("-topmost", 1)
    test()
    
    config=ConfigParser()
    config.SECTCRE = re.compile(r"\[ *(?P<header>[^]]+?) *\]")
    config.optionxform = lambda option: option
    config.read('..\config\com.ini')
    p=re.compile(r'\s*,\s*')
   
    #print(config.sections())
    #print(config.items('bytesize'))
    #print(dict(config.items('bytesize')))
    #xconfig.sections()
    #xconfig.remove('default')
    config.remove_section('default')
    print(
          dict(
               map(
                   lambda m:[m,dict(config.items(m))],
                   #xconfig
                   config.sections()
                   )
               )
          )
    
    x=list(range(5))
    print(x)
    print(x.remove(3)==None)
    print(x)

        
    

    root.mainloop()