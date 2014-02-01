import fs_wrapper
import settings.common as SC
from qrd_shared.case import *
from case_utility import *
from test_case_base import TestCaseBase
import time
import logging_wrapper

class test_suit_stability_ui_case9(TestCaseBase):
    def test_case_main(self, case_results):

        repeat_times = int(SC.PUBLIC_CASE_REPEAT_NUMBER)
        total_times = 0
        total_success = 0
        
        for i in range(0, repeat_times):
            flag1 = False
            
            try:
                set_can_continue()
                total_times = total_times+1
                #long press power button
                send_key(KEYCODE_POWER, LONG_PRESS)
                time.sleep(1)
                
                if search_text('Power off' and 'Airplane mode', searchFlag=TEXT_CONTAINS):
                    flag1 = True
                else:
                    flag1 = False
                goback()
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
            time.sleep(3)

        qsst_log_msg(str(total_success) + '/' + str(total_times))
        print_report_line("Total:" +str(total_success) + '/' + str(total_times),)