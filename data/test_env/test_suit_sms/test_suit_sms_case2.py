import fs_wrapper
import settings.common as SC
from qrd_shared.case import *
from case_utility import *
from test_case_base import TestCaseBase
import time
import logging_wrapper

class test_suit_sms_case2(TestCaseBase):
    def test_case_main(self, case_results):
        
        sms_num = SC.PUBLIC_SLOT2_NUMBER
        sms_text=SC.PUBLIC_MESSAGE_CONTENTS
        sms_repeat_times = int(SC.PRIVATE_SMS_REPEAT_NUMBER)
        total_times = 0
        total_success = 0
        sms_slot = 1
        time_after_off = int(SC.PRIVATE_AIRPLANEMODE_TIME_AFTER_MODE_OFF)
        
        #turn off airplane mode
        launcher.launch_from_launcher("settings")
        settings.turn_off_airplane(time_after_off)
        
        for i in range(0, sms_repeat_times):
            flag1 = False

            try:
                set_can_continue()
                total_times = total_times+1
                launcher.launch_from_launcher("mms")
                flag1 = mms.sms(sms_num, sms_slot, sms_text)
            except Exception as e:
                '''if an exception occurs,we will set the status of this case to fail'''
                #str_context = get_context_info()
                qsst_log_msg(str(i+1) + '\texception' + '\t' + time.strftime('%X',time.localtime(time.time())))
                log_test_framework('Test','Exception' + str(e))
                save_fail_log()
            
            if flag1:
                #qsst_log_case_status(logging_wrapper.STATUS_SUCCESS, 'voice call success', logging_wrapper.SEVERITY_HIGH)
                total_success = total_success+1
            else:
                #qsst_log_case_status(logging_wrapper.STATUS_FAILED, 'voice call failed', logging_wrapper.SEVERITY_HIGH)
                qsst_log_msg(str(i+1) + '\tfail' + '\t' + time.strftime('%X',time.localtime(time.time())))
                save_fail_log()
            
            sleep(3)

        qsst_log_msg(str(total_success) + '/' + str(total_times))
        print_report_line("Total:" +str(total_success) + '/' + str(total_times),)

def format_phone_number(num):
    s = insert(num, ' ', 3)
    return insert(s, ' ', 8)

def insert(original, new, pos):
    '''Inserts new inside original at pos.'''
    return original[:pos] + new + original[pos:]
