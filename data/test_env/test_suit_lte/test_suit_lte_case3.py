import fs_wrapper
import settings.common as SC
from case_utility import *
from test_case_base import TestCaseBase
from qrd_shared.case import *
import logging_wrapper
import time


class test_suit_lte_case3(TestCaseBase):
    def test_case_main(self, case_results):
        mms_num = SC.PUBLIC_SLOT1_NUMBER
        mms_text=SC.PUBLIC_MESSAGE_CONTENTS
        test_repeat_times = SC.PUBLIC_CASE_REPEAT_NUMBER
        mms_attachment = SC.PRIVATE_MTMMS_MTMMS_ATTACHMENT
        mms_intervaltime="40"
        mms_waittime = 60
        call_number_slot1 = '02161037643'
        call_slot = 0
        call_duration = 60
        total_success = 0
        total_times = 0
        interval = 30
        for i in range(0,int(test_repeat_times)):
            flag1 = False
            flag2 = False
            try:
                set_can_continue()
                total_times = total_times+1
                #Delete all threads
                launcher.launch_from_launcher("settings")
                settings.enableDATA()
                launcher.launch_from_launcher("mms")
                flag1 = mms.mms(mms_num, 0, mms_text)
                launcher.launch_from_launcher("phone")
                flag2 = phone.phone_call(call_number_slot1, call_slot, call_duration)
            except Exception as e:
                '''if an exception occurs,we will set the status of this case to fail'''
                #str_context = get_context_info()
                qsst_log_msg(str(i+1) + '\texception' + '\t' + time.strftime('%X',time.localtime(time.time())))
                log_test_framework('Test','Exception'+str(e))
                save_fail_log()
            if flag1 & flag2:
                total_success = total_success+1
            else:
            #qsst_log_case_status(logging_wrapper.STATUS_FAILED, 'voice call failed', logging_wrapper.SEVERITY_HIGH)
                qsst_log_msg(str(i+1) + '\tfail' + '\t' + time.strftime('%X',time.localtime(time.time())))
                save_fail_log()
            
            sleep(interval)
                
        qsst_log_msg(str(total_success) + '/' + str(total_times))
        print_report_line("Total:" +str(total_success) + '/' + str(total_times),)