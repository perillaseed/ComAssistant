from tkinter import *
from tkinter.simpledialog import askstring
from tkinter.font import Font
import time
import binascii

MOVE_LINES = 0
MOVE_PAGES = 1
MOVE_TOEND = 2

bin2formatx={
             'String' :lambda data: data.decode('ascii'),
             'Bin'      :lambda data: ' '.join(i[2:].rjust(8,'0') for i in list(map(bin,data))),
             'Hex'      :lambda data: ' '.join([''.join(list(map(chr,list(zip(*[iter(binascii.b2a_hex(data))]*2))[i]))) for i in range(len(data))]),
             'Oct'      :lambda data: ' '.join(i[2:].rjust(3,'0') for i in list(map(oct,data))),
             'Dec'      :lambda data: ' '.join(list(map(repr,map(ord,data.decode())))),
             'Bytes'    :lambda data: data
             }

time2formatx={'24h':lambda data:data,
              '12h':lambda data:data
              }

class MultiListbox(Frame):
    def __init__(self, master, columns, font=None,*cnf, **kws):
        Frame.__init__(self, master,*cnf,**kws)
        self.lists = []
        self.master=master
        
        if font:
            self.txtFont=font
        else:
            self.txtFont=Font(family="Arial", size=14)
        self.defaultRowHeight=self.txtFont['size']+7
        
        self.txshow=StringVar(master)
        self.rxshow=StringVar(master)
        
        self.variables={}
        self.showlistboxs(columns)        
        
    def showlistboxs(self,columns):
        for name,w,*options in columns:
            canvas=Canvas(self, height=self.defaultRowHeight+2, bd=0,highlightthickness=0, bg='white')
            canvas.pack(side=LEFT,expand=YES,fill=BOTH)
            
            frame=Frame(canvas)
            frame.pack(side=TOP,expand=YES,fill=X)
            
            #optionmenu=OptionMenu(canvas, self.variables[name],*options)
            #optionmenu.config(width=2,borderwidth=1, relief=RAISED, bg='GRAY',height=1)           
            #optionmenu.pack(side=TOP,expand=NO,fill=X)
            
            button=Button(frame,text=name)
            button.config(width=2,borderwidth=1, relief=RAISED, bg='GRAY',height=1)
            button.pack(side=LEFT,expand=YES,fill=X)
            #button.bind('<Button-1>', lambda e:self.popup(e))
            
            spinbox=Spinbox(frame,wrap=True,from_=0,to=200,width=3)
            spinbox.delete(0,END)
            spinbox.insert(END,w)
            spinbox.pack(side=LEFT,expand=NO,fill=X)

            self.variables[name]=StringVar()
            self.variables[name].set(name)
            
            lb = Listbox(canvas, 
                        width=w, 
                        borderwidth=0, 
                        selectborderwidth=0,
                        relief=FLAT, 
                        exportselection=False,
                        bg='WHITE',
                        selectmode=EXTENDED)
            lb.pack(side=TOP,expand=YES, fill=BOTH)
            
            xsb = Scrollbar(canvas, orient=HORIZONTAL)
            xsb.pack(expand=NO, fill=X,side=TOP)
            xsb.config(command=lb.xview)
            lb.config(xscrollcommand=xsb.set)

            spinbox.config(command=lambda spinbox=spinbox,lb=lb: lb.config(width=int(spinbox.get())))
            self.lists.append(lb)
            lb.bind('<B1-Motion>', lambda e, s=self: s._select(e.y))
            lb.bind('<Button-1>', lambda e, s=self: s._select(e.y))
            lb.bind('<Leave>', lambda e: 'break')
            lb.bind('<B2-Motion>', lambda e, s=self: s._b2motion(e.x, e.y))
            lb.bind('<Button-2>', lambda e, s=self: s._button2(e.x, e.y))
            lb.bind('<Button-3>', lambda e,s=self:s.popup(e))
            lb.bind('<Double-1>',lambda e,s=self,lb=lb: s.modify(lb))
            #lb.bind('<Button-4>', lambda e, s=self: s._scroll(SCROLL, -1, UNITS))
            #lb.bind('<Button-5>', lambda e, s=self: s._scroll(SCROLL, 1, UNITS))

 
        self.bind ('<Up>',    lambda e, s=self: s._move (-1, MOVE_LINES))
        self.bind ('<Down>',  lambda e, s=self: s._move (+1, MOVE_LINES))
        self.bind ('<Prior>', lambda e, s=self: s._move (-1, MOVE_PAGES))
        self.bind ('<Next>',  lambda e, s=self: s._move (+1, MOVE_PAGES))
        self.bind ('<Home>',  lambda e, s=self: s._move (-1, MOVE_TOEND))
        self.bind ('<End>',   lambda e, s=self: s._move (+1, MOVE_TOEND))
        
        self.bind('<Control-c>', lambda e, s=self: s.copy())
        self.bind('<Control-v>', lambda e, s=self: s.insert(int(s.curselection()[0]),self.copied))
        self.bind('<Control-x>', lambda e, s=self: s.cut())
        
        self.bind('<Insert>', lambda e, s=self: s.insert(int(s.curselection()[0]),list(map(lambda x:'',range(len(s.lists))))))        
        self.bind('<Delete>', lambda e, s=self: s.delete(int(s.curselection()[0])))
        
        self.bind("<MouseWheel>", lambda e, s=self : s.mouseScroll)
        
        yframe = Frame(self)
        yframe.pack(side=LEFT, expand=NO, fill=Y)
        Label(yframe, borderwidth=1, relief=RAISED).pack(side=TOP,expand=NO,fill=X)
        ysb = Scrollbar(yframe, orient=VERTICAL, command=self._scroll)
        ysb.pack(side=TOP,expand=YES, fill=Y)
        self.lists[0]['yscrollcommand']=ysb.set
        
        self.copied=list(map(lambda x:'',range(len(self.lists))))
        
        self.defaultCursor=self.cget("cursor")
        
 
    def _move (self, lines, relative=0):
        """
        Move the selection a specified number of lines or pages up or
        down the list.    Used by keyboard navigation.
        """
        selected = self.lists[0].curselection()
        try:
            selected = list(map(int, selected))
        except ValueError:
            pass
 
        try:
            sel = selected[0]
        except IndexError:
            sel = 0
 
        old     = sel
        size = self.lists [0].size()
         
        if relative == MOVE_LINES:
            sel = sel + lines
        elif relative == MOVE_PAGES:
            sel = sel + (lines * int (self.lists [0]['height']))
        elif relative == MOVE_TOEND:
            if lines < 0:
                sel = 0
            elif lines > 0:
                sel = size - 1
        else:
            print("MultiListbox._move: Unknown move type!")
 
        if sel < 0:
            sel = 0
        elif sel >= size:
            sel = size - 1
         
        self.selection_clear (old, old)
        self.see (sel)
        self.selection_set (sel)
        return 'break'
 
    def _select(self, y):
        row = self.lists[0].nearest(y)
        self.selection_clear(0, END)
        self.selection_set(row)
        self.focus_force()
        return 'break'
 
    def _button2(self, x, y):
        for l in self.lists:
            l.scan_mark(x, y)
        return 'break'
 
    def _b2motion(self, x, y):
        for l in self.lists:
            l.scan_dragto(x, y)
        return 'break'
 
    def _scroll(self, *args):
        for l in self.lists:
            l.yview(*args)
        return 'break'
        
    def _xscroll(self, *args):
        for l in self.lists:
            l.yview(*args)
        return 'break'
    
    def yview(self,*args):
        for l in self.lists:
            l.yview(*args)
        
        
    def enterColEnd(self, event):
        self.canvas.configure(cursor='sb_h_double_arrow')

    def leaveColEnd(self, event):
        self.canvas.configure(cursor=self.defaultCursor)

    def startDrag(self, event):
        self.wgt1=self.canvas.find_withtag('current')
        self.currCol=self.columns[int(self.canvas.gettags(self.wgt1)[1])]
        self.startX=self.canvas.bbox(self.wgt1)[0]
        self.canvas.bind('<B1-Motion>', self.moveBorder)
        self.canvas.bind('<ButtonRelease>', self.stopMoveBorder)

    def moveBorder(self, event):
        self.canvas.tag_raise(self.wgt1)
        wgt_x=self.canvas.bbox(self.wgt1)[0]
        diff=event.x-wgt_x
        self.canvas.move(self.wgt1, diff, 0)

    def stopMoveBorder(self, event):
        self.canvas.unbind('<B1-Motion>')
        self.canvas.unbind('<ButtonRelease>')
        self.grab_release()
        wgt_x=self.canvas.bbox(self.wgt1)[0]
        change=wgt_x-self.startX
        self.currCol['width']+=change
        self.show()
        
    def mouseScroll(self, event):
        if event.delta >0:
            for l in self.lists:
                l.yview("scroll", "-1", "units")
        else:
            for l in self.lists:
                l.yview("scroll", "1", "units")
 
    def curselection(self):
        return self.lists[0].curselection()
 
    def itemconfigure(self, row_index, col_index, cnf=None, **kw):
        lb = self.lists[col_index]
        return lb.itemconfigure(row_index, cnf, **kw)
 
    def rowconfigure(self, row_index, cnf={}, **kw):
        for lb in self.lists:
            lb.itemconfigure(row_index, cnf, **kw)
 
    def delete(self, first, last=None):
        for l in self.lists:
            l.delete(first, last)
            l.selection_set(first-1)
            #l.activate(first-1)
 
    def get(self, first, last=None):
        result = []
        for l in self.lists:
            result.append(l.get(first,last))
        #if last:
        #     return map(*([None] + result))
        return result
 
    def index(self, index):
        self.lists[0].index(index)
        
    def config(self,**options):
        for l in self.lists:
            l.config(**options)
            
    def itemconfig(self,index,**options):
        for l in self.lists:
            l.itemconfig(index,**options)
 
    def insert(self, index, *elements):        
        for e in elements:
            i = 0
            for l in self.lists:
                l.insert(index, e[i])
                i = i + 1
                l.yview(index)
 
    def size(self):
        return self.lists[0].size()
 
    def see(self, index):
        for l in self.lists:
            l.see(index)
 
    def selection_anchor(self, index):
        for l in self.lists:
            l.selection_anchor(index)
 
    def selection_clear(self, first, last=None):
        for l in self.lists:
            l.selection_clear(first, last)
 
    def selection_includes(self, index):
        return self.lists[0].selection_includes(index)
 
    def selection_set(self, first, last=None):
        for l in self.lists:
            l.selection_set(first, last)
 
    def yview_scroll(self, *args, **kwargs):
        for lb in self.lists:
            lb.yview_scroll(*args, **kwargs)
            
    def copy(self):
        self.copied=self.get(int(self.curselection()[0]))
        #print(self.copied)
        
    def cut(self):
        self.copy()
        self.delete(int(self.curselection()[0]))
        
    def modify(self,lb):
        index=self.curselection()[0]
        data=askstring(title='修改',prompt='请输入字符串',initialvalue=lb.get(index))
        if data != None:
            lb.delete(index)
            lb.insert(index,data)
            
    def popup(self,e):
        menu = Menu(self.master, tearoff=0)
        menu.add_command(label="复制", command=lambda s=self: s.copy())
        menu.add_command(label="剪切", command=lambda s=self: s.cut())
        menu.add_command(label="粘贴", command=lambda s=self: s.insert(int(s.curselection()[0]),self.copied))
        menu.add_command(label="插入", command=lambda s=self: s.insert(int(s.curselection()[0]),list(map(lambda x:'',range(len(s.lists))))))
        menu.add_command(label="删除", command=lambda s=self: s.delete(int(s.curselection()[0])))
        menu.post(e.x_root, e.y_root)
            
if __name__=='__main__':
    root = Tk()
    Label(root, text='MultiListbox').pack()
    Entry(root).pack()
    #columns=(('time', 18), ('Transited', 20), ('Received', 20))
    columns=[['time',18,'time','seconds'],
             ['Transited',20,'String','Bin','Oct','Hex'],
             ['Received',20,'String','Bin','Oct','Hex']
             ]
    mlb = MultiListbox(root, columns)
    for i in range(1000):
        mlb.insert(END, ('%s' %time.strftime('%H:%M:%S %Y-%m-%d'), 'John Doe %d' % i, '10/10/%04d' % (1900+i)))
    mlb.pack(expand=YES,fill=BOTH)
    root.mainloop()
    
    