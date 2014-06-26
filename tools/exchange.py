'''
Created on 2013年8月30日

@author: Seed
'''


import binascii
import os,sys

import socket
import time
import struct

formatx2bin={
             'String' :lambda data: data.encode('ascii'),
             'Bin'      :lambda data: ''.join(map(chr,[int(data[i:i+8],2) for i in range(0,len(data),8)])).encode('ascii'),
             'Hex'      :lambda data: binascii.a2b_hex(data),
             'Oct'      :lambda data: ''.join(map(chr,[int(data[i:i+3],8) for i in range(0,len(data),3)])).encode('ascii'),
             'Dec'      :lambda data: int(data,10),
             }

bin2formatx={
             'String' :lambda data: data.decode('ascii'),
             'Bin'      :lambda data: ' '.join(i[2:].rjust(8,'0') for i in list(map(bin,data))),
             'Hex'      :lambda data: ' '.join([''.join(list(map(chr,list(zip(*[iter(binascii.b2a_hex(data))]*2))[i]))) for i in range(len(data))]),
             'Oct'      :lambda data: ' '.join(i[2:].rjust(3,'0') for i in list(map(oct,data))),
             'Dec'      :lambda data: ' '.join(list(map(repr,map(ord,data.decode())))),
             'Bytes'    :lambda data: data
             }

# global definition
# base = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, A, B, C, D, E, F]
base = [str(x) for x in range(10)] + [ chr(x) for x in range(ord('A'),ord('A')+6)]

class Exchange():
    '''
    classdocs
    '''
    

    @classmethod
    def __init__(self,source):
        '''
        Constructor
        '''
        self.source=source
    @classmethod            
    def bin2hex(cs,source):
        return hex(int(source, 2)) 
    @classmethod    
    def bin2dec(cs,source):
        return int(source, 2)    
    @classmethod            
    def bin2oct(cs,source):
        return oct(int(source, 2))
    
     
    @classmethod            
    def oct2hex(cs,source):
        return hex(int(source, 8)) 
    @classmethod    
    def oct2dec(cs,source):
        return int(source, 8)    
    @classmethod            
    def oct2bin(cs,source):
        return bin(int(source, 10)) 
    
    
    
    @classmethod            
    def dec2hex(cs,source):
        return hex(int(source, 10)) 
    @classmethod    
    def dec2oct(cs,source):
        return oct(int(source, 10))    
    @classmethod            
    def dec2bin(cs,source):
        return bin(int(source, 10)) 
    
    
    @classmethod            
    def hex2dec(cs,source):
        return int(source.upper(), 16) 
    @classmethod    
    def hex2oct(cs,source):
        return oct(int(source.upper(), 16))    
    @classmethod            
    def hex2bin(cs,source):
        return bin(int(source.upper(), 16)) 
    
    @classmethod
    def ip2hex (cs,ip):
        return hex(struct.unpack("!I", socket.inet_aton(ip))[0])
    @classmethod
    def ip2long (cs,ip):
        return struct.unpack("!I", socket.inet_aton(ip))[0]    
    @classmethod
    def long2ip (cs,lint):
        return socket.inet_ntoa(struct.pack("!I", lint))
    
def test(lists):
    for x in lists:
        print(x,'bin2dec', Exchange.bin2dec(x))
        print(x,'hex2dec', Exchange.hex2dec(x))
        print(x,'dec2bin', Exchange.dec2bin(x))
        print(x,'dec2hex', Exchange.dec2hex(x))
        print(x,'hex2bin', Exchange.hex2bin(x))
        print(x,'bin2hex', Exchange.bin2hex(x))
        
def splitCount(s, count):
    return [''.join(x) for x in zip(*[list(s[z::count]) for z in range(count)])]
 
def split_len(seq, length):
    return [seq[i:i+length] for i in range(0, len(seq), length)]

        
def exchange(source):
    pass

def check(s,S):  
    try:
        global source
        source.set(adjust(s+S))
        return True
    except Exception as e:
        print(e)
        return False

def adjust(data):
    #data=entry.get()
    if len(data)%2 is 0:
        data=data
    else:
        data=data[0:-1]+'0'+data[-1:]
    source.set(binascii.a2b_hex(data))
    print(binascii.a2b_hex(data))        
    return binascii.a2b_hex(data)

    
if __name__=='__main__':
    blists=['1111','0001','0000']    
    #test(blists)
    
    from tkinter import *
    root=Tk()
    
    source=StringVar()
    
    vcmd = (root.register(check), '%s', '%S')
    label=Label(root,textvariable=source)
    label.pack()
    entry=Entry(root,
                #textvariable=source,
                validate="key",
                vcmd=vcmd
                )
    entry.bind('<Key>',lambda e:adjust(source.get()))
    entry.pack()
    
    button=Button(root,text='print!')
    button.pack()
    
    listbox=Listbox(root)
    listbox.pack(side=LEFT)
    
    scrollbar=Scrollbar(root,orient=VERTICAL)
    scrollbar.pack(side=LEFT,expand=NO,fill=Y)
    
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)
    
    button.config(command=lambda :listbox.insert(END,entry.get()))  
    root.mainloop()
    
    
    
    
    
    
    
    