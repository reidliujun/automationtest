from case_utility import *
from qrd_shared.Base import Base
from qrd_shared.language.language import Language
import time
from qrd_shared.launcher import Launcher

############################################
#author:
#    yileiwan@cienet.com.cn
#function:
#    Open gallery.
#doc:
############################################

class Gallery(Base):
    def __init__(self):
        self.mode_name = "gallery"
        Base.__init__(self,self.mode_name)
        self.debug_print( 'Base init:%f' %(time.time()))