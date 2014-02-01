import fs_wrapper
import settings.common as SC
from case_utility import *
from test_case_base import TestCaseBase
from qrd_shared.case import *
import logging_wrapper
import time


class test_suit_phone_case2(TestCaseBase):
    def test_case_main(self, case_results):

        call_number = SC.PUBLIC_SLOT2_NUMBER
        call_repeat_times = int(SC.PRIVATE_PHONE_REPEAT_NUMBER)
        call_duration = int(SC.PRIVATE_PHONE_CALL_DURATION)
        interval = int(SC.PRIVATE_PHONE_INTERVAL)
        call_slot = 1
        total_times = 0
        total_success = 0
        time_after_off = int(SC.PRIVATE_AIRPLANEMODE_TIME_AFTER_MODE_OFF)
        call_delay = 0

#        #turn off airplane mode
#        launcher.launch_from_launcher("settings")
#        settings.turn_off_airplane(time_after_off)

        for i in range(0,call_repeat_times):
            flag1 = False
            
            try:
                set_can_continue()
                total_times = total_times+1
                launcher.launch_from_launcher("phone")
                flag1 = phone.phone_call(call_number, call_slot, call_duration)
                print phone.call_delay
            except Exception as e:
                '''if an exception occurs,we will set the status of this case to fail'''
                #str_context = get_context_info()
                qsst_log_msg(str(i+1) + '\texception' + '\t' + time.strftime('%X',time.localtime(time.time())))
                log_test_framework('Test','Exception' + str(e))
                save_fail_log()
                #return

            if flag1:
                #qsst_log_case_status(logging_wrapper.STATUS_SUCCESS, 'voice call success', logging_wrapper.SEVERITY_HIGH)
                #qsst_log_msg(str(i+1) + '\tsuccess' + '\t' + time.strftime('%X',time.localtime(time.time())))
                total_success = total_success+1
            else:
                #qsst_log_case_status(logging_wrapper.STATUS_FAILED, 'voice call failed', logging_wrapper.SEVERITY_HIGH)
                qsst_log_msg(str(i+1) + '\tfail' + '\t' + time.strftime('%X',time.localtime(time.time())))
                save_fail_log()
            
            sleep(interval)

        qsst_log_msg(str(total_success) + '/' + str(total_times))
        print_report_line("Total:" +str(total_success) + '/' + str(total_times),)