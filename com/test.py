from tkinter import *
from com.kthread import KThread
import time
from threading import Timer

class UpdateThread(KThread):
    def __init__(self,func,*args):
        KThread.__init__(self)
        self.func=func
        self.args=args
        
        
    def run(self):
        #ser = serial.Serial('COM1',9600)
        #while True:
        self.func(*self.args)
        time.sleep(0.001)

def test(delay=0.5,index=100,data=['a','b','c']):
    for i in range(index):
        print(i)
        print(data)
        time.sleep(delay)
        
    
    
            
if __name__=='__main__':
    root=Tk()
    
    testthread=UpdateThread(test,0.5,100,['d','e','f'])
    testthread.daemon=True
    
    
    Button(root,text='start',command=lambda : testthread.start()).pack()
    Button(root,text='stop',command=lambda : testthread.kill()).pack()
    
    root.mainloop()

        
            
            
        
