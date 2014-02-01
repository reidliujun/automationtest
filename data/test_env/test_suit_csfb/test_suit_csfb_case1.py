import fs_wrapper
import settings.common as SC
from case_utility import *
from test_case_base import TestCaseBase
from qrd_shared.case import *
import logging_wrapper
'''
Voice call+continuous Ping
"1. Ping ftp server continuously
2. Make a MT voice call
3. End the call"
by L. Jun 0704/2013
'''
class test_suit_csfb_case1(TestCaseBase):
    def test_case_main(self, case_results):
        #mt call
        call_number_slot1 = SC.PUBLIC_LOCAL_SLOT1_NUMBER
        call_repeat_times = SC.PUBLIC_CASE_REPEAT_NUMBER
        call_duration = SC.PRIVATE_MTCALL_DURATION
        waittime = SC.PRIVATE_MTCALL_WAIT_TIME
        intervaltime = SC.PRIVATE_MTCALL_INTERVAL
        
        try:
            set_can_continue()
            launcher.launch_from_launcher("settings")
            settings.disable_wifi()
            settings.enableDATA()
            osInfo = get_platform_info()
            if(osInfo == "Windows" or osInfo == "Linux-PC"):
                subprocess.Popen(["adb", "shell", "ping -w 7200 8.8.8.8 &"])
            elif(osInfo == "Linux-Phone"):
                os.system("ping -w 30 8.8.8.8 &")
            launcher.launch_from_launcher("mtservice")
            phone.mtcall(call_number_slot1, call_repeat_times, call_duration, waittime, intervaltime)
#            os.system("ping -w 30 8.8.8.8")
        except Exception as e:
            '''if an exception occurs,we will set the status of this case to fail'''
            #str_context = get_context_info()
            qsst_log_msg('\texception' + '\t' + time.strftime('%X',time.localtime(time.time())))
            log_test_framework('Test','Exception')
            save_fail_log()
        t=0
        while(1):
            time.sleep(1)
            t=t+1
            if (search_view_by_id("endButton")):
                t=0
            elif (t>60):
                print t
                break
        if isAliveforProcess("ping"):
            kill_by_name("ping")