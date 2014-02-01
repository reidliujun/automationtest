import fs_wrapper
import settings.common as SC
from qrd_shared.case import *
from case_utility import *
from test_case_base import TestCaseBase
import time
import logging_wrapper

class test_suit_stability_ui_case15(TestCaseBase):
    def test_case_main(self, case_results):

        repeat_times = int(SC.PUBLIC_CASE_REPEAT_NUMBER)
        time_after_on = int(SC.PRIVATE_AIRPLANEMODE_TIME_AFTER_MODE_ON)
        time_after_off = int(SC.PRIVATE_AIRPLANEMODE_TIME_AFTER_MODE_OFF)
        call_number_1 = SC.PUBLIC_SLOT1_NUMBER
        call_duration = int('1')
        call_slot_1 = 0
        total_times = 0
        total_success = 0
        
        for i in range(0, repeat_times):
            flag1 = False
            
            try:
                set_can_continue()
                total_times = total_times+1
                #Make a MO call
                launcher.launch_from_launcher("phone")
                result1 = phone.dial(call_number_1, call_slot_1, call_duration)
                if not result1:
                    qsst_log_case_status(logging_wrapper.STATUS_FAILED, 'voice call failed', logging_wrapper.SEVERITY_HIGH)
                    return
                
                #Turn on airplane mode
                launcher.launch_from_launcher("settings")
                result2 = settings.turn_on_airplane(time_after_on, time_after_off)
                if not result2:
                    qsst_log_case_status(logging_wrapper.STATUS_FAILED, 'airplane mode failed', logging_wrapper.SEVERITY_HIGH)
                    return
                
                #Check phone status
                launcher.launch_from_launcher("phone")
                flag1 = phone.check_call_status()
                
                #Turn off airplane mode
                launcher.launch_from_launcher("settings")
                settings.turn_off_airplane(time_after_off)
            except Exception as e:
                '''if an exception occurs,we will set the status of this case to fail'''
                #str_context = get_context_info()
                qsst_log_msg(str(i+1) + '\texception' + '\t' + time.strftime('%X',time.localtime(time.time())))
                log_test_framework('Test','Exception' + str(e))
                save_fail_log()
            
            if not flag1:
                #qsst_log_case_status(logging_wrapper.STATUS_SUCCESS, 'voice call success', logging_wrapper.SEVERITY_HIGH)
                total_success = total_success+1
            else:
                #qsst_log_case_status(logging_wrapper.STATUS_FAILED, 'voice call failed', logging_wrapper.SEVERITY_HIGH)
                qsst_log_msg(str(i+1) + '\tfail' + '\t' + time.strftime('%X',time.localtime(time.time())))
                save_fail_log()
            sleep(3)

        qsst_log_msg(str(total_success) + '/' + str(total_times))
        print_report_line("Total:" +str(total_success) + '/' + str(total_times),)