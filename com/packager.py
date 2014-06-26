'''
Created on 2013年9月8日

@author: Seed
'''
import time
import threading
import re
from configparser import ConfigParser,RawConfigParser,SafeConfigParser


import binascii

import logging
import logging.config
#logging.basicConfig(format='%(levelname)s %(asctime)s %(module)s %(funcName)s %(lineno)d %(message)s', datefmt='%Y-%m-%d %H:%M:%S',level=logging.DEBUG)
#logger=logging.getLogger(__name__)
logging.config.fileConfig('..\config\logging.ini',disable_existing_loggers=False)
logger = logging.getLogger('xlogger')

class Packager(object):
    '''
    classdocs
    '''
    

    def __init__(self,file='..\config\packager.ini',packerstyle='default',*cnf,**kws):
        '''
        Constructor
        '''
        
        self.styles={}
        self.sections={}
        self.getini(file,packerstyle)
        
        self.number=0
        #pass
        
    def getini(self,file='..\config\packager.ini',packerstyle='default'):
        config=ConfigParser()
        config.SECTCRE = re.compile(r"\[ *(?P<header>[^]]+?) *\]")
        config.optionxform = lambda option: option
        config.read(file)        
        p=re.compile(r'\s*,\s*')        
        print(config.sections())
        
        try:
            self.sections=dict(config.items('default',raw=True))
        except Exception as e:
            logger.error(e)
        logger.debug(self.sections)
        #'''
        for section in self.sections:
            self.sections[section]=eval(self.sections[section])
        #'''
        logger.debug(self.sections)
        
        for style in config.sections():
            if style is not 'default':
                self.styles[style]=dict(map(lambda m:[m,p.split(dict(config.items(style))[m])],dict(config.items(style))))
        logger.debug(self.styles)

    def pack(self,data,style='basic'):
        packed={}
        for element in self.styles[style]['withoutdata']:
            packed[element]=self.sections[element]()
        for element in self.styles[style]['withdata']:
            packed[element]=self.sections[element](data)
        packed['tail']=eval(self.styles[style]['tail'][0])
        self.number=self.sections['number'](self.number)
        packed['number']=str(self.number)
        return packed

    def unpack(self,data,style='basic'):
        #print(self.styles['basic']['sequence'])
        unpacked=[]
        for element in self.styles[style]['sequence']:            
            #print(element)
            #print(data[element])            
            unpacked.append(data[element])
            
        #return eval(self.styles[self.style]['connector'][0]).join(data)
        return unpacked

            
    
if __name__=='__main__':
    data=b'abc'
    packer=Packager('..\config\packager.ini','basic')
    packed=packer.pack(data)
    #packed={'time': 'Tue Sep 10 10:39:50 2013', 'data': 'abc', 'threadname': 'MainThread', 'tail': '\n', 'hexdata': '61 62 63'}
    #print(packer.packed)
    unpacked=packer.unpack(packed)
    #print(packer.unpacked)
    print(unpacked)
    
