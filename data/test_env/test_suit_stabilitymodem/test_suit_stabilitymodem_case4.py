'''
Modem scenarios test case 6--case 12
created by L. JUN
03/06/2013
'''
import fs_wrapper
import settings.common as SC
from case_utility import *
from test_case_base import TestCaseBase
from qrd_shared.case import *
import logging_wrapper
import time


class test_suit_stabilitymodem_case4(TestCaseBase):
    def test_case_main(self, case_results):
        dsds_flag = SC.PUBLIC_DSDS
        call_repeat_times_slot = int(SC.PUBLIC_CASE_REPEAT_NUMBER)
        call_duration = 1200 #1200
        interval = 3600 #3600
        total_times = 0
        total_success = 0
        
        for i in range(0,call_repeat_times_slot):
            total_times = total_times+1
            flag1 = False
            ''' 
                if dual card, call on slot2.
            '''
            if dsds_flag == False:
                call_number_slot = SC.PUBLIC_SLOT1_NUMBER
                call_slot = 0
            else:
                call_number_slot = SC.PUBLIC_SLOT2_NUMBER
                call_slot = 1
                
            try:
                set_can_continue()
                launcher.launch_from_launcher("phone")
                flag1 = phone.phone_call(call_number_slot, call_slot, call_duration)
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