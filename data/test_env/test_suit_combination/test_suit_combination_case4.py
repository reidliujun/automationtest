import fs_wrapper
from qrd_shared.case import *
from case_utility import *
from utility_wrapper import *
from test_case_base import TestCaseBase
import settings.common as SC
import logging_wrapper

class test_suit_combination_case4(TestCaseBase):
    TAG = "test_suit_combination_case4"
    def test_case_main(self, case_results):

        total_times = 0
        total_success = 0
        repeat_times=int(SC.PUBLIC_CASE_REPEAT_NUMBER)
        call_number_slot1 = SC.PUBLIC_SLOT1_NUMBER
        slot = 1
        call_duration = int(SC.PRIVATE_PHONE_CALL_DURATION)
        
        for i in range(0, repeat_times):
            flag1 = False
            
            try:
                set_can_continue()
                total_times = total_times+1

                # long ping
                osInfo = get_platform_info()
                if(osInfo == "Windows" or osInfo == "Linux-PC"):
                    os.system("adb shell ping -w 60 8.8.8.8 &")
                elif(osInfo == "Linux-Phone"):
                    os.system("ping -w 60 8.8.8.8 &")
                sleep(60)
                # kill "ping" if still exit
                if isAliveforProcess("ping"):
                    kill_by_name("ping")

                #MO call
                launcher.launch_from_launcher("phone")
                flag1 = phone.phone_call(call_number_slot1, slot, call_duration)
    
                if flag1:
                    total_success = total_success+1
                else:
                    qsst_log_msg(str(i+1) + '\tfail' + '\t' + time.strftime('%X',time.localtime(time.time())))
                    save_fail_log()
            except Exception as e:
                '''if an exception occurs,we will set the status of this case to fail'''
                #str_context = get_context_info()
                qsst_log_msg(str(i+1) + '\texception' + '\t' + time.strftime('%X',time.localtime(time.time())))
                log_test_framework('Test','Exception' + str(e))
                save_fail_log()
            
            sleep(3)

        qsst_log_msg(str(total_success) + '/' + str(total_times))
        print_report_line("Total:" +str(total_success) + '/' + str(total_times))