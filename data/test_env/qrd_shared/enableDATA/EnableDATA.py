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
class EnableDATA(Base):
    TAG = "EnableDATA"
    def __init__(self):
        self.mode_name = "enableDATA"
        Base.__init__(self,self.mode_name)
        self.debug_print( 'EnableDATA init:%f' %(time.time()))
        