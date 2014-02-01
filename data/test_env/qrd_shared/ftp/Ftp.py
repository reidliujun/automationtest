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
class Ftp(Base):
    TAG = "AndFTP"
    def __init__(self):
        self.mode_name = "ftp"
        Base.__init__(self,self.mode_name)
        self.debug_print( 'AndFTP init:%f' %(time.time()))
        
    def add_ftp(self,address,port,username,password):
        click_textview_by_text(self.get_value("add"))
        sleep(4)
        entertext_edittext_by_index(0,address)
        entertext_edittext_by_index(1,port)
        entertext_edittext_by_index(2,username)
        entertext_edittext_by_index(3,password) 
        