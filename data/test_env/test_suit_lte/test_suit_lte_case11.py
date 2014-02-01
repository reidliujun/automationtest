import fs_wrapper
import settings.common as SC
from case_utility import *
from test_case_base import TestCaseBase
from qrd_shared.case import *
import logging_wrapper
import time


class test_suit_lte_case11(TestCaseBase):
    def test_case_main(self, case_results):
        total_success = 0
        repeat_times = int(SC.PUBLIC_CASE_REPEAT_NUMBER)
#        repeat_times = 1
        flag1 = [False]*repeat_times
        flag2 = False
        launcher.launch_from_launcher("settings")
        settings.disable_wifi()
        settings.enableDATA()
        (5)
            
        t=0
        while(t<repeat_times):
            #=======================================================================
            # start ping
            #=======================================================================
            osInfo = get_platform_info()
            if(osInfo == "Windows" or osInfo == "Linux-PC"):
                subprocess.Popen(["adb", "shell", "ping -s 500 8.8.8.8 &"])
            elif(osInfo == "Linux-Phone"):
                os.system("ping -s 500 8.8.8.8 &")
            time.sleep(60)
            #===================================================================
            # check ping status every minute, last repeat_times minutes
            #===================================================================
            if isAliveforProcess("ping"):
                flag1[t] = True
                kill_by_name("ping")
            else:
                flag1[t] = False
                time_error=time.strftime('%X',time.localtime(time.time()))
                qsst_log_msg(str(t+1)+'ping stop:' + '\t' + time_error)
            if t==0:
                flag2 = flag1[t]
            else:
                flag2 = flag1[t] & flag2
            print flag1[t]
            print flag2
            t=t+1
        #=======================================================================
        # Stop ping
        #=======================================================================
        if isAliveforProcess("ping"):
            kill_by_name("ping")
        if flag2:
            total_success = total_success+1
        else:
            save_fail_log()
            
        qsst_log_msg(str(total_success) + '/' + str(repeat_times))
        print_report_line("Total:" +str(total_success) + '/' + str(repeat_times),)
#            
            