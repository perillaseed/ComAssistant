'''
Created on 2013年9月2日

@author: Seed
'''

class Filters():
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''


    def __new__(self):
        self.elements={}
        self.elements['Bin']=lambda key:self.isbin(key)
        self.elements['Oct']=lambda key:self.isoct(key)
        self.elements['Dec']=lambda key:self.isdec(key)
        self.elements['Hex']=lambda key:self.ishex(key)
        self.elements['String']=lambda key:self.isstring(key)

        return self.elements
        
    @staticmethod
    def isdec(key):
        return key.isdigit()        
  
    @staticmethod
    def ishex(key):
        return key in ('0','1','2','3','4','5','6','7','8','9',
                       'A','B','C','D','E','F',
                       'a','b','c','d','e','f')
    
    @staticmethod
    def isbin(key):
        return key in ('0','1')
    
    @staticmethod    
    def isoct(key):
        return key in ('0','1','2','3','4','5','6','7')
    
    @staticmethod    
    def isstring(key):
        return key.isalnum()
        
if __name__=='__main__':
    filter=Filters()
    x=filter['Bin'](b'2')
    print(x)
            
        
        