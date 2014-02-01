import fs_wrapper
import settings.common as SC
from qrd_shared.case import *
from case_utility import *
from test_case_base import TestCaseBase
import time
import logging_wrapper

class test_suit_mtmms_case1(TestCaseBase):
    def test_case_main(self, case_results):

        mms_num = SC.PUBLIC_LOCAL_SLOT1_NUMBER
        mms_text=SC.PUBLIC_MESSAGE_CONTENTS
        mms_repeat_times = SC.PRIVATE_MTMMS_MTMMS_REPEAT_TIMES
#        mms_attachment = SC.PRIVATE_MTMMS_MTMMS_ATTACHMENT
        intervaltime = int(SC.PRIVATE_MTMMS_MTMMS_INTERVAL)
        
        try:
            set_can_continue()
            #Delete all threads
            launcher.launch_from_launcher("settings")
            settings.disable_wifi()
            settings.enableDATA()
#            launcher.launch_from_launcher("mms")
#            
#            click_imageview_by_index(0)
#            sleep(2)
#            delete_all_threads = "Delete all threads"
#            mms.delete_all_threads()
            
#            launcher.launch_from_launcher("mtservice")
#            mms.mtmms(mms_num, mms_text, mms_repeat_times, mms_attachment, intervaltime)
#            t= int(intervaltime)*int(mms_repeat_times)
#            sleep(t)
            for i in range(0,mms_repeat_times):
    #           mt_trigger_service_sms(msg_title_text, to, interval, time_out, count=1, msg_type=0, wap_url=" ")
                mt_trigger_service_sms(mms_text, mms_num, intervaltime, 30, count=1, msg_type=1, wap_url=" ")
                sleep(intervaltime)
        except Exception as e:
            '''if an exception occurs,we will set the status of this case to fail'''
            #str_context = get_context_info()
            qsst_log_msg('\texception' + '\t' + time.strftime('%X',time.localtime(time.time())))
            log_test_framework('Test','Exception' + str(e))
            save_fail_log()