'''
Created on 2013年7月30日

@author: Seed
'''

import logging

from logging import handlers,config


import sys
import time
import argparse



def usage():
    print("Usage:")


def getopt(argv):
    parser = argparse.ArgumentParser(prog='logger',
                                     description='''多行测试信息
    --------
多行测试信息
******
多行测试信息
''',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     usage='%(prog)s [options]',
                                     epilog='''
多行测试信息
    --------
多行测试信息
******
多行测试信息
'''
                                     )
    parser.add_argument('-c', '--clog',
                        type=str,
                        choices=['DEBUG','INFO','WARNING','ERROR','CRITICAL'],
                        default='DEBUG',
                        help='控制台日志输出级别'
                        )
    parser.add_argument('-f', '--flog',
                        type=str,
                        choices=['DEBUG','INFO','WARNING','ERROR','CRITICAL'],
                        default='DEBUG',
                        help='文件日志输出级别'
                        )
    parser.add_argument('-t','--test',
                        type=str,  #type=open, 可以用于打开文件
                        #default='sample',
                        #dest='xtest',   #起一个别名
                        help='测试')
    #parser.print_help()  #测试打印出的帮助信息
    args = parser.parse_args()
    
    #logger.debug(args)
    #print(vars(args))  #命名空间字典化
    #print(vars(args)['log'])
    return vars(args)
    

def testlog():
    '''
    Test log function.
    '''  
    #测试信息
    logger.info('Info message!')
    logger.debug('Debug message!')
    logger.warning('Warning message!')
    logger.error('Error message!')
    logger.critical('Critical message!')

if __name__=='__main__':
    
    #%(asctime)——————时间
    #%(name)—————————日志模块名称（handler）
    #%(levelname)————日志级别
    #%(pathname)—————源文件绝对路径
    #%(module)———————程序模块名称
    #%(funcName)—————程序函数名称
    #%(lineno)———————源文件代码行号
    #%(message)——————日志信息
    logger=logging.getLogger(__name__)
    FORMAT='\
%(asctime)s\t\
%(name)s\t\
%(levelname)s\t\
%(pathname)s\t\
%(lineno)d\t\
%(module)s\t\
%(funcName)s\t\
%(message)s\t'

    

    
              
    logging.basicConfig(
                        filename='test.log',            #日志文件名称
                        filemode='w',                   #文件打开模式
                        level=logging.DEBUG,            #日志记录级别
                        #level=getopt(sys.argv[1:])['clog'],
                        format=FORMAT,                  #日志文件格式
                        datefmt='%j %Y/%m/%d %H:%M:%S %p %X', #时间格式
                        converter=time.localtime(),
                        #utc=True,
                        backup_count = 5, 
                        limit = 20480,
                        when=None)

    
    
    
       
    logger.info(sys.argv[:])    
    #logger.log(logging.INFO, 'test info message!')    
    #testlog()
    #logging.info('test logging information')    
    logger.setLevel(getopt(sys.argv[1:])['flog'])
    #testlog()
    
    chandler=logging.StreamHandler()
    chandler.setLevel(getopt(sys.argv[1:])['clog'])
    chandler.setFormatter(logging.Formatter(FORMAT))
    logger.addHandler(chandler)
    
    
    
    
    fhandler=logging.handlers.TimedRotatingFileHandler(
                                                       'flog.log',
                                                       when='M',
                                                       interval=5,
                                                       backupCount=0,
                                                       utc=False         #文件名使用UTC时间标识
                                                       )
    xfhandler=logging.handlers.RotatingFileHandler('xflog.log',
                                                   mode='a',
                                                   maxBytes=10240,
                                                   backupCount=10
                                                   )                  
    xfhandler.setLevel(getopt(sys.argv[1:])['flog'])
    xfhandler.setFormatter(logging.Formatter(FORMAT))
    logger.addHandler(xfhandler)
    
    fhandler.setLevel(getopt(sys.argv[1:])['flog'])
    fhandler.setFormatter(logging.Formatter(FORMAT))
    logger.addHandler(fhandler)
    
    i=100
    while i > 0:
        i=i-1
        time.sleep(0.5)     
        testlog()
    
    
    
    


    
    
    