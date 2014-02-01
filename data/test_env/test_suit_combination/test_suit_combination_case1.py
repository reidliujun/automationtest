import fs_wrapper
from qrd_shared.case import *
from case_utility import *
from utility_wrapper import *
from test_case_base import TestCaseBase
import settings.common as SC
import logging_wrapper
import time

class test_suit_combination_case1(TestCaseBase):
    TAG = "test_suit_combination_case1"
    def test_case_main(self, case_results):

        total_times = 0
        total_success = 0
        slot = 1
        call_duration = int(SC.PRIVATE_PHONE_CALL_DURATION)
        repeat_times=int(SC.PUBLIC_CASE_REPEAT_NUMBER)
        mms_num = SC.PUBLIC_SLOT1_NUMBER
        mms_text = SC.PUBLIC_MESSAGE_CONTENTS
        call_number_slot1 = SC.PUBLIC_SLOT1_NUMBER

        for i in range(0, repeat_times):
            flag1 = False
            flag2 = False
            flag3 = False
            
            try:
                set_can_continue()
                total_times = total_times+1
                
                # MO CALL
                launcher.launch_from_launcher("phone")
                flag1 = phone.phone_call(call_number_slot1, slot, call_duration)
                if not flag1:
                    qsst_log_case_status(logging_wrapper.STATUS_FAILED, 'voice call failed', logging_wrapper.SEVERITY_HIGH)
                    continue
                    
                # MO MMS
                launcher.launch_from_launcher("mms")
                flag2 = mms.mms(mms_num, slot, mms_text)
                if not flag2:
                    qsst_log_msg(str(i+1) + '\tmms fail' + '\t' + time.strftime('%X',time.localtime(time.time())))
                    continue
    
                # MO SMS
                launcher.launch_from_launcher("mms")
                flag3 = mms.sms(mms_num, slot, mms_text)
                if not flag3:
                    qsst_log_msg(str(i+1) + '\tsms fail' + '\t' + time.strftime('%X',time.localtime(time.time())))
                    continue
    
                if flag1 & flag2 & flag3:
                    total_success = total_success+1

            except Exception as e:
                '''if an exception occurs,we will set the status of this case to fail'''
                #str_context = get_context_info()
                qsst_log_msg(str(i+1) + '\texception' + '\t' + time.strftime('%X',time.localtime(time.time())))
                log_test_framework('Test','Exception' + str(e))
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
