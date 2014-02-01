#coding=utf-8
from case_utility import *
from qrd_shared.Base import Base
from logging_wrapper import log_test_framework
import time

############################################
#author:
#    chuanchunyu@cienet.com.cn
#function:
#    the settings mode of qrd share lib.
#doc:
############################################
class Streaming(Base):
    TAG = "Streaming"
    def __init__(self):
        self.mode_name = "streaming"
        Base.__init__(self,self.mode_name)
        self.debug_print( 'Streaming init:%f' %(time.time()))
