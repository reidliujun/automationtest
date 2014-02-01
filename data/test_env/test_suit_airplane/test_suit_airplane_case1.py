import fs_wrapper
import settings.common as SC
from case_utility import *
from test_case_base import TestCaseBase
from qrd_shared.case import *
import logging_wrapper
import time

class test_suit_airplane_case1(TestCaseBase):
    def test_case_main(self, case_results):
        
        time_after_on = int(SC.PRIVATE_AIRPLANEMODE_TIME_AFTER_MODE_ON)
        time_after_off = int(SC.PRIVATE_AIRPLANEMODE_TIME_AFTER_MODE_OFF)
        repeat_times = int(SC.PRIVATE_AIRPLANEMODE_REPEAT_NUMBER)
        call_number_1 = SC.PUBLIC_SLOT1_NUMBER
        call_number_2 = SC.PUBLIC_SLOT2_NUMBER
        call_duration = int('5')
        call_slot_1 = 0
        call_slot_2 = 1
        total_times = 0
        total_success = 0
        
        for i in range(0, repeat_times):
            flag1 = False
            
            try:
                set_can_continue()
                total_times = total_times+1
                
                launcher.launch_from_launcher("settings")
                settings.set_airplane(time_after_on,time_after_off)

                launcher.launch_from_launcher("phone")
                flag1 = phone.phone_call(call_number_1, call_slot_1, call_duration)

                if SC.PUBLIC_DSDS:
                    launcher.launch_from_launcher("phone")
                    flag2 = phone.phone_call(call_number_2, call_slot_2, call_duration)
    
                    if flag1 == True and flag2 == True:
                        #qsst_log_case_status(logging_wrapper.STATUS_SUCCESS, 'voice call success', logging_wrapper.SEVERITY_HIGH)
                        total_success = total_success+1
                    else:
                        #qsst_log_case_status(logging_wrapper.STATUS_FAILED, 'voice call failed', logging_wrapper.SEVERITY_HIGH)
                        qsst_log_msg(str(i+1) + '\tfail' + '\t' + time.strftime('%X',time.localtime(time.time())))
                        save_fail_log()
                else:
                    if flag1 == True:
                        #qsst_log_case_status(logging_wrapper.STATUS_SUCCESS, 'voice call success', logging_wrapper.SEVERITY_HIGH)
                        total_success = total_success+1
                    else:
                        #qsst_log_case_status(logging_wrapper.STATUS_FAILED, 'voice call failed', logging_wrapper.SEVERITY_HIGH)
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