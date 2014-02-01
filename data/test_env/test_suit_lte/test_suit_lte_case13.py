import fs_wrapper
import settings.common as SC
from case_utility import *
from test_case_base import TestCaseBase
from qrd_shared.case import *
import logging_wrapper
import time


class test_suit_lte_case13(TestCaseBase):
    def test_case_main(self, case_results):
        total_times = 0
        total_success = 0
        call_number_slot1 = SC.PUBLIC_LOCAL_SLOT1_NUMBER
        call_repeat_times = SC.PUBLIC_CASE_REPEAT_NUMBER
        call_duration = '120'
        waittime = '20'
        intervaltime = '150'
        t = 150*int(call_repeat_times)+60
        try:
            set_can_continue()
            launcher.launch_from_launcher("settings")
            settings.disable_wifi()
            settings.enableDATA()
            launcher.launch_from_launcher("autoanswerapp")
            phone.call_autoanswer_enable()
            osInfo = get_platform_info()
            if(osInfo == "Windows" or osInfo == "Linux-PC"):
                subprocess.Popen(["adb", "shell", "ping -w 7200 -s 500 8.8.8.8 &"])
            elif(osInfo == "Linux-Phone"):
                os.system("ping -w 7200 -s 500 8.8.8.8 &")
            launcher.launch_from_launcher("mtservice")
            phone.mtcall(call_number_slot1, call_repeat_times, call_duration, waittime, intervaltime)
            sleep(t)
            if isAliveforProcess("ping"):
                kill_by_name("ping")
            launcher.launch_from_launcher("autoanswerapp")
            phone.call_autoanswer_disable()
        except Exception as e:
            '''if an exception occurs,we will set the status of this case to fail'''
            #str_context = get_context_info()
            log_test_framework('Test','Exception' + str(e))
            save_fail_log()
        qsst_log_msg(str(total_success) + '/' + str(total_times))
        print_report_line("Total:" +str(total_success) + '/' + str(total_times),)