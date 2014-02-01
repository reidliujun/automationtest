import fs_wrapper
import settings.common as SC
from qrd_shared.case import *
from case_utility import *
from test_case_base import TestCaseBase
import time
import logging_wrapper

class test_suit_stability_ui_case12(TestCaseBase):
    def test_case_main(self, case_results):

        repeat_times = int(SC.PUBLIC_CASE_REPEAT_NUMBER)
        time_after_on = int(SC.PRIVATE_AIRPLANEMODE_TIME_AFTER_MODE_ON)
        time_after_off = int(SC.PRIVATE_AIRPLANEMODE_TIME_AFTER_MODE_OFF)
        sms_num = SC.PUBLIC_SLOT1_NUMBER
        sms_text=SC.PUBLIC_MESSAGE_CONTENTS
        slot = 0
        total_times = 0
        total_success = 0
        
        for i in range(0, repeat_times):
            flag1 = False
            
            try:
                set_can_continue()
                total_times = total_times+1
                #Turn on airplane mode
                launcher.launch_from_launcher("settings")
                result = settings.turn_on_airplane(time_after_on, time_after_off)
                if not result:
                    qsst_log_case_status(logging_wrapper.STATUS_FAILED, 'airplane mode open failed', logging_wrapper.SEVERITY_HIGH)
                    return

                #Make a MO SMS
                launcher.launch_from_launcher("mms")
                flag1 = mms.sms(sms_num, slot, sms_text)
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