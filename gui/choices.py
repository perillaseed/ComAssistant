import sys
from tkinter import *
from com.comx import Com
from configparser import ConfigParser
import serial
import time
import threading
import binascii
import string
from tkinter.simpledialog import messagebox

vcmds={
             'String' :lambda key: key,
             'Bin'      :lambda key: key in ('0','1'),
             'Hex'      :lambda key: key in string.hexdigits,
             'Oct'      :lambda key: key in string.octdigits,
             'Dec'      :lambda key: key in string.digits,
             }

formatx2bin={
             'String' :lambda data: data.encode('ascii'),
             'Bin'      :lambda data: ''.join(map(chr,[int(data[i:i+8],2) for i in range(0,len(data),8)])).encode('ascii'),
             'Hex'      :lambda data: binascii.a2b_hex(data),
             'Oct'      :lambda data: ''.join(map(chr,[int(data[i:i+3],8) for i in range(0,len(data),3)])).encode('ascii'),
             'Dec'      :lambda data: int(data,10),
             }


class Choices(Frame):
    def __init__(self,master,options=None, *cnf,**kws):
        Frame.__init__(self, master,*cnf,**kws)
        self.choice=StringVar()
        self.choice.set('String')
        self.rawdata=StringVar()
      
        self.rawdata=self.showOpts(master,*cnf,**kws)
        #self.data=formatx2bin[self.choice.get()](self.rawdata.get())
        
        self.values=[]        
        self.values.append(self.choice)
        self.values+=self.showAutos(master,'延时(毫秒)',*cnf,**kws)
        self.values+=self.showAutos(master,'重复(次数)', *cnf,**kws)
        self.values.append(self.rawdata)
        #self.decision(master,**cnf)
        

    def showOpts(self,master,options=vcmds.keys()):
        okayCommand = self.register(self.isOK)
        self.choice=StringVar()
        self.choice.set('String')
        
        frameOpts=Frame(master)
        frameOpts.pack(expand=YES,fill=X)
        for option in sorted(options):
            radiobutton=Radiobutton(frameOpts, 
                        text=option.center(8), 
                        justify=LEFT,
                        variable=self.choice,
                        value=option,
                        width=4,
                        )
            radiobutton.pack(side=LEFT,fill=X,expand=YES)
            radiobutton.config(command=lambda radiobutton=radiobutton:self.transform())
        
        rawdata=StringVar()        
        self.entry=Entry(master,
                    textvariable=rawdata,
                    validate='key',
                    validatecommand=(okayCommand,'%d','%i','%s','%S'))
        
        self.entry.pack(fill=X,expand=YES)
        return rawdata
                  
    def showAutos(self,master,text,*cnf,**kws):
        checkstatus=IntVar()
        frameAutos=Frame(master)
        frameAutos.pack(side=LEFT,expand=YES,fill=X)
        
        spinbox=Spinbox(frameAutos,
                from_=0,
                to=99999999,
                state=DISABLED
                )
        checkbutton=Checkbutton(frameAutos,
                    text = text,
                    variable=checkstatus,
                    onvalue = 1,
                    offvalue = 0,
                    command=lambda signal=checkstatus,widget=spinbox: self.toggleAutos(signal,widget) 
                    )
        
        checkbutton.pack(side=LEFT,
                           fill=X,
                           expand=YES
                           )
        spinbox.pack(side=LEFT,
                      fill=X,
                      expand=YES
                      )
        return [checkstatus,spinbox]
    
    def toggleAutos(self,signal,widget):
        if signal.get()==1:
            widget.config(state=NORMAL)
        else:
            widget.config(state=DISABLED)
            
    def toggleChoices(self):        
        for key in self.entries.keys():
            self.entries[key].config(state='readonly')
        self.entries[self.choice.get()].config(state=NORMAL)
        
    def transform(self):
        self.entry.select_clear()
        self.rawdata.set('')

     
    def get(self):
        try:            
            values=[]
            for value in self.values:
                values.append(value.get())
            self.data=formatx2bin[self.choice.get()](self.rawdata.get())    
            values.append(self.data)
            return dict(zip(['choice','delaystate','delaytime','repeatstate','repeattime','rawdata','data'],values))                
        except Exception as e:
            messagebox.showerror('出错啦！', e)
            return 'break'
        #return values
    
    def isOK(self,d,i,s,S):
        self.entry.select_clear()
        if vcmds[self.choice.get()](S):
            return True
        else:
            return False
        
if __name__=='__main__':
    root=Tk()
    
    Button(root,
       text='Go!',
       command=lambda : print(choices.get())
       ).pack(side=BOTTOM,
              fill=X,
              expand=YES
              )
    
    choices=Choices(root)
    choices.pack(side=TOP,expand=YES,fill=X)  
    #print(choices.get())
    root.bind('<Return>', lambda e : print(choices.get()))

    root.mainloop()