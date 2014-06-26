from tkinter import *
import time

from com.comx import Com
from com.kthread import *
from gui.sendWin import SendWin
from gui.configWin import ConfigWin
from gui.recvWin import RecvWin



class MainWin(Frame):
    def __init__(self,master,widget,*cnf,**kws):
        Frame.__init__(self,master)
        
        
        self.showConfigWin(master,*cnf,**kws)     
        self.showRecvWin(master,*cnf,**kws)
        self.showSendWin(master,*cnf,**kws)
        
        self.sending=None
        self.checkstatus(widget)

        #self.com=self.configwin.com
        #self.ser=self.configwin.ser        
        
    def showConfigWin(self,master,comlist=Com.getList(),*cnf,**kws):
        frameConfigWin=Frame(master)
        frameConfigWin.pack(side=TOP,expand=YES,fill=X)
        
        #from gui.configWin import ConfigWin
       
        self.configwin=ConfigWin(master=frameConfigWin,coms=comlist)
        self.configwin.pack(side=TOP,expand=YES,fill=X)
    
    def showRecvWin(self,master,*cnf,**kws):
        recvframe=Frame(master)
        recvframe.pack(side=TOP,expand=YES,fill=X)
        
        #from gui.recvWin import RecvWin
        
        self.recvwin=RecvWin(recvframe,self.configwin)
        self.recvwin.pack() 
        
    def showSendWin(self,master,*cnf,**kws):
        sendframe=Frame(master)
        sendframe.pack(side=TOP,expand=YES,fill=X)
        
        self.sendwin=SendWin(sendframe)
        self.sendwin.pack()
        
    def send(self):
        data=self.sendwin.choices.get()['data']
        delaystate=self.sendwin.choices.get()['delaystate']
        repeatstate=self.sendwin.choices.get()['repeatstate']
        delaytime=int(self.sendwin.choices.get()['delaytime'])/1000 if delaystate is 1 else 0       
        repeattime=int(self.sendwin.choices.get()['repeattime']) if repeatstate is 1 else 1
        if self.recvwin.com is not None:
            if self.recvwin.com.isOpen():
                if data is not b'': 
                    for i in range(repeattime):                    
                        self.recvwin.com.send(data)
                        time.sleep(delaytime)
                    self.sendwin.choices.entry.delete(0, END)
                self.sending=None                    
            else:
                messagebox.showinfo('出错啦！', '串口被关了吧？')
        else:
            messagebox.showwarning('出错啦！', '忘了开串口了吧！')
            
    def togglesend(self,event,widget):
        if self.sending is None:
            self.sending=KThread(target=self.send)
            self.sending.daemon=True
            self.sending.start()
        else:
            self.sending.kill()
            self.sending=None
    
    def checkstatus(self,widget):
        if self.sending is None:
            widget.config(bg='GREEN')
        else:
            widget.config(bg='RED')
        self.after(100, self.checkstatus,(widget))

if __name__ == '__main__':
    root=Tk()
    
    root.title('串口助手')
    
    button=Button(root,text='Go!')
    mainwin=MainWin(root,button)
    
    mainwin.pack(expand=YES,fill=X,side=TOP)    
    
    button.bind('<Button-1>',lambda event,widget=button:mainwin.togglesend(event,widget))
    button.pack(expand=YES,fill=X,side=TOP)
    
    root.bind('<Return>',lambda event,widget=button:mainwin.togglesend(event,widget))
    root.mainloop()
