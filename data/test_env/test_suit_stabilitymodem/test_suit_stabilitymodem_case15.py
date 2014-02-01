'''
Modem scenarios test case 76
created by L. JUN
06/06/2013
'''
import fs_wrapper
import settings.common as SC
from case_utility import *
from test_case_base import TestCaseBase
from qrd_shared.case import *
import logging_wrapper
import time
'''
wifi hot pot test
'''

class test_suit_stabilitymodem_case15(TestCaseBase):
    def test_case_main(self, case_results):
        # long ping in background
        osInfo = get_platform_info()
        if(osInfo == "Windows" or osInfo == "Linux-PC"):
            subprocess.Popen(["adb", "shell", "ping -w 7200 8.8.8.8 &"])
        elif(osInfo == "Linux-Phone"):
            os.system("ping -w 7200 8.8.8.8 &")
        # sleep
        sleep(7200)
        # kill "ping" if still exit
        if isAliveforProcess("ping"):
            kill_by_name("ping")
