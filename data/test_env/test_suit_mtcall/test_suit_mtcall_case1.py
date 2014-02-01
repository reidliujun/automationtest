import fs_wrapper
import settings.common as SC
from case_utility import *
from test_case_base import TestCaseBase
from qrd_shared.case import *
import logging_wrapper

class test_suit_mtcall_case1(TestCaseBase):
    def test_case_main(self, case_results):
        #mt call
        call_number_slot1 = SC.PUBLIC_LOCAL_SLOT1_NUMBER
        call_repeat_times = int(SC.PRIVATE_MTCALL_REPEAT_TIMES)
        call_duration = int(SC.PRIVATE_MTCALL_DURATION)
        waittime = int(SC.PRIVATE_MTCALL_WAIT_TIME)
        intervaltime = int(SC.PRIVATE_MTCALL_INTERVAL)
        
        try:
            set_can_continue()
            launcher.launch_from_launcher("settings")
            settings.disable_wifi()
            settings.enableDATA()
            launcher.launch_from_launcher("autoanswerapp")
            phone.call_autoanswer_enable()
#            launcher.launch_from_launcher("mtservice")
#            phone.mtcall(call_number_slot1, call_repeat_times, call_duration, waittime, intervaltime)
#            mt_trigger_service_call(to, wait_time, hold_time, interval, num_of_calls=1, count_off=True)
            for i in range(0,call_repeat_times):
                mt_trigger_service_call(call_number_slot1, waittime, call_duration, intervaltime, num_of_calls=1, count_off=True)
                sleep(intervaltime)
        except Exception as e:
            '''if an exception occurs,we will set the status of this case to fail'''
            #str_context = get_context_info()
            qsst_log_msg('\texception' + '\t' + time.strftime('%X',time.localtime(time.time())))
            log_test_framework('Test','Exception' + str(e))
            save_fail_log()
#        t=0
#        while(1):
#            time.sleep(1)
#            t=t+1
#            if (search_view_by_id("endButton")):
#                t=0
#            elif (t>60):
#                print t
#                break
        launcher.launch_from_launcher("autoanswerapp")
        phone.call_autoanswer_disable()