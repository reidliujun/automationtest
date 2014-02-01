import fs_wrapper
import settings.common as SC
from case_utility import *
from test_case_base import TestCaseBase
from qrd_shared.case import *
import logging_wrapper
import time


class test_suit_lte_case14(TestCaseBase):
    def test_case_main(self, case_results):
        call_number = '02161037644'
        call_duration = int(SC.PRIVATE_LTE_LONGCALL_TIME)
        interval = 30
        call_slot = 0
        total_times = 0
        total_success = 0
        try:
            launcher.launch_from_launcher("settings")
            settings.disable_wifi()
            settings.enableDATA()
            sleep(5)
            set_can_continue()
            total_times = total_times+1
            #===============================================================
            # Start Ping
            #===============================================================
            osInfo = get_platform_info()
            if(osInfo == "Windows" or osInfo == "Linux-PC"):
                subprocess.Popen(["adb", "shell", "ping -w 7200 -s 500 8.8.8.8 &"])
            elif(osInfo == "Linux-Phone"):
                os.system("ping -w 7200 -s 500 8.8.8.8 &")
            #===========================================================
            # MO call
            #===========================================================
            launcher.launch_from_launcher("phone")
            flag1 = phone.phone_call(call_number, call_slot, call_duration)
            flag2 = isAliveforProcess("ping")
            if flag2:
                kill_by_name("ping")
        except Exception as e:
            '''if an exception occurs,we will set the status of this case to fail'''
            #str_context = get_context_info()
            qsst_log_msg('\texception' + '\t' + time.strftime('%X',time.localtime(time.time())))
            log_test_framework('Test','Exception' + str(e))
            save_fail_log()
