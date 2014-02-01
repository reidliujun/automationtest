'''
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
Data scenario
'''

class test_suit_stabilitymodem_case16(TestCaseBase):
    def test_case_main(self, case_results):
        try:
            if SC.PUBLIC_DSDS:
                launcher.launch_from_launcher("settings")
                settings.disable_wifi()
                settings.enableDATA()
                settings.set_default_data(2)
                sleep(5)
                for i in range(0,100):
                #===================================================================
                # ping
                #===================================================================
                    osInfo = get_platform_info()
                    if(osInfo == "Windows" or osInfo == "Linux-PC"):
                        subprocess.Popen(["adb", "shell", "ping -w 7200 8.8.8.8 &"])
                    elif(osInfo == "Linux-Phone"):
                        os.system("ping -w 7200 8.8.8.8 &")
                    sleep(60)
                    if isAliveforProcess("ping"):
                            kill_by_name("ping")
            else:
                qsst_log_msg('test_suit_stabilitymodem_case10 is DSDS test case' + time.strftime('%X',time.localtime(time.time())))

        except Exception as e:
            qsst_log_msg('\texception' + '\t' + time.strftime('%X',time.localtime(time.time())))
            log_test_framework('Test','Exception' + str(e))
            save_fail_log()