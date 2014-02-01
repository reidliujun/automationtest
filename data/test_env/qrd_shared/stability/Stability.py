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
class Stability(Base):
    TAG = "Stability"
    def __init__(self):
        self.mode_name = "stability"
        Base.__init__(self,self.mode_name)
        self.debug_print( 'Stability init:%f' %(time.time()))
