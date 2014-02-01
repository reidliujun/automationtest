'''
Modem scenarios test case 6 - case 8
Multiparty call
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
Multiparty call
'''

class test_suit_stabilitymodem_case13(TestCaseBase):
    def test_case_main(self, case_results):
        call_number1 = SC.PUBLIC_SLOT1_NUMBER
        call_number2 = SC.PUBLIC_SLOT2_NUMBER
        call_repeat_times_slot1 = int(SC.PUBLIC_CASE_REPEAT_NUMBER)
        call_duration = 45
        interval = 30
        call_slot = 0
        total_times = 0
        total_success = 0
        

        for i in range(0,call_repeat_times_slot1):
            flag1 = False
            total_times = total_times+1
            try:
                set_can_continue()
                launcher.launch_from_launcher("phone")
                flag1 = phone.phone_call_multiparty(call_number1, call_number2, call_slot, call_duration)
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