'''
Created on 2013年8月24日

@author: Seed
'''
import time, signal
from multiprocessing import Process,Lock
from tkinter import *



class TxProcess(Process):
    '''
    classdocs
    '''


    def __init__(self, gap):
        '''
        Constructor
        '''
        Process.__init__(self)
        #self.widget=widget
        self.gap=gap

        
    def run(self):
        #print(self.name)
        self.flash(self.gap)       
        return
    
    def flash(self,gap):
        
        
        for i in range(gap):
            '''
            widget.config(bg='YELLOW',text=i)
            time.sleep(0.5)
            widget.config(bg='BLACK',text=i)
            time.sleep(0.5)
            '''
            print(i)



x=None
def test(gap):
    global x
    print(x)
    if x!=None:
        print(x,'will be stop!')        
        x.terminate()
        x.join()
        print(x.exitcode)
        x=None
    else:
        x=TxProcess(gap)
        print(x,'will be start!')
        x.start()
        #x.join()
    
if __name__=='__main__':
    
    root=Tk()
    lock = Lock()
    frame=Frame(root)
    frame.pack()
    
    button2=Button(frame,text='kill',bg='GREEN')
    
    button=Button(frame,text='start',bg='YELLOW')
    
    
    button.config(command=lambda :test(100000000))
    button.pack()
    
    button2.config(command=lambda :test(100000000))
    button2.pack()
    
    root.mainloop()
        
        