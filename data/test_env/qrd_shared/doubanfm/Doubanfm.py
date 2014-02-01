from case_utility import *
from qrd_shared.Base import Base
from qrd_shared.language.language import Language
import time
############################################
#author:
#    lihuang@cienet.com.cn
#function:
#    the doubanfm mode of qrd share lib.
#doc:
############################################
class Doubanfm(Base):

    def __init__(self):
        self.mode_name = "doubanfm"
        Base.__init__(self,self.mode_name)
        self.debug_print( 'Base init:%f' %(time.time()))
