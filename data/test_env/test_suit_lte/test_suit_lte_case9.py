import fs_wrapper
import settings.common as SC
from case_utility import *
from test_case_base import TestCaseBase
from qrd_shared.case import *
import logging_wrapper
import time
'''
Procedure:
"1  Power up the UE and verify the device camps on a operator network. 
2  Trigger Manual PLMN search.  
3  Select a PLMN (different - compared to what was used in step-1 above)  
4  Repeat above steps"
'''

class test_suit_lte_case9(TestCaseBase):
    def test_case_main(self, case_results):
        total_times = 0
        total_success = 0
        time_after_search=int(SC.PRIVATE_PLMN_TIME_AFTER_SEARCH)
        repeat_times=int(SC.PUBLIC_CASE_REPEAT_NUMBER)

        for i in range(0, repeat_times):
            flag1 = False

            try:
                set_can_continue()
                total_times = total_times+1
                launcher.launch_from_launcher("settings")
                flag1 = settings.set_plmnsearch(0,time_after_search)
            except Exception as e:
                '''if an exception occurs,we will set the status of this case to fail'''
                #str_context = get_context_info()
                qsst_log_msg(str(i+1) + '\texception' + '\t' + time.strftime('%X',time.localtime(time.time())))
                log_test_framework('Test','Exception' + str(e))
                save_fail_log()
            
            if flag1 == True:
                #qsst_log_case_status(logging_wrapper.STATUS_SUCCESS, 'voice call success', logging_wrapper.SEVERITY_HIGH)
                total_success = total_success+1
            else:
                #qsst_log_case_status(logging_wrapper.STATUS_FAILED, 'voice call failed', logging_wrapper.SEVERITY_HIGH)
                qsst_log_msg(str(i+1) + '\tfail' + '\t' + time.strftime('%X',time.localtime(time.time())))
                save_fail_log()
            sleep(3)

        qsst_log_msg(str(total_success) + '/' + str(total_times))
        print_report_line("Total:" +str(total_success) + '/' + str(total_times),)