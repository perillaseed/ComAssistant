'''
Created on 2013年9月14日

@author: Seed
'''
from configparser import ConfigParser,RawConfigParser,SafeConfigParser
import re


if __name__=='__main__':
    config=ConfigParser()
    config.SECTCRE = re.compile(r"\[ *(?P<header>[^]]+?) *\]")
    config.optionxform = lambda option: option
    config.read('..\config\packager.ini')
    p=re.compile(r'\s*,\s*')
    print(config.sections())
    styles={}
    for style in config.sections():
        if style is not 'default':
            print(style)
            styles[style]=dict(map(lambda m:[m,p.split(dict(config.items(style))[m])],dict(config.items(style)))) 
            print(styles[style])

    
    
        
        