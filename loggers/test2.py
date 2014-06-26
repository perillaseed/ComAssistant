'''
Created on 2013年8月5日

@author: Seed
'''
import logging
import logging.config
import time
from color import print


def testlog(logger):
    '''
    Test log function.
    '''  
    #测试信息
    logger.info('Info message!')
    logger.debug('Debug message!')
    logger.warning('Warning message!')
    logger.error('Error message!')
    logger.critical('Critical message!')




if __name__ == '__main__':
    
    #print('hello', 'world!', color='blue')
    #print('hello', 'world!', color='red')
    logging.config.fileConfig('logging.ini',disable_existing_loggers=False)
    

    # create logger
    '''
    logging.getLogger('debug')
    logging.getLogger('debug.info')
    logger = logging.getLogger('debug.info.warning')
    '''
    logger = logging.getLogger('xlogger')
    
    i=1
    while i > 0:
        i=i-1
        testlog(logger)
        
    logging.shutdown()   
