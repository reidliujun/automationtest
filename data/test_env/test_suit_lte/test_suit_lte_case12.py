import fs_wrapper
import settings.common as SC
from case_utility import *
from test_case_base import TestCaseBase
from qrd_shared.case import *
import logging_wrapper
import time


class test_suit_lte_case12(TestCaseBase):
    def test_case_main(self, case_results):
        repeat_times = int(SC.PUBLIC_CASE_REPEAT_NUMBER)
        call_number = SC.PUBLIC_SLOT2_NUMBER
        call_duration = 10
        interval = 30
        call_slot = 0
        total_times = 0
        total_success = 0
        launcher.launch_from_launcher("settings")
        settings.disable_wifi()
        settings.enableDATA()
        (5)
        for i in range(0,repeat_times):
            flag1 = False
            flag2 = False
            try:
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
                if flag1 & flag2:
                    total_success = total_success+1
                else:
                    qsst_log_msg(str(i+1) + '\tfail' + '\t' + time.strftime('%X',time.localtime(time.time())))
                    save_fail_log()
                sleep(interval)
            except Exception as e:
                '''if an exception occurs,we will set the status of this case to fail'''
                #str_context = get_context_info()
                qsst_log_msg(str(i+1) + '\texception' + '\t' + time.strftime('%X',time.localtime(time.time())))
                log_test_framework('Test','Exception' + str(e))
                save_fail_log()
            
        qsst_log_msg(str(total_success) + '/' + str(total_times))
        print_report_line("Total:" +str(total_success) + '/' + str(total_times),)