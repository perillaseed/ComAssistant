'''
Created on 2013年8月7日

@author: Seed
'''

from configparser import ConfigParser
import re

class Ininfo(ConfigParser):
    '''
    classdocs
    '''


    def __init__(self,fname='logging.ini'):
        '''
        Constructor
        '''
        self.config=ConfigParser()
        self.config.SECTCRE = re.compile(r"\[ *(?P<header>[^]]+?) *\]")
        self.config.optionxform = lambda option: option
        self.config.read(fname)
        #p=re.compile(r'\s*,\s*')
        
    def listkeys(self,section):
        return re.compile(r'\s*,\s*').split(self.config[section]['keys'])
    


if __name__=='__main__':
    for section in ['loggers','handlers','formatters']:
        print(Ininfo('logging.ini').listkeys(section))
        