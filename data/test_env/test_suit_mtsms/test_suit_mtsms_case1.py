import fs_wrapper
import settings.common as SC
from case_utility import *
from test_case_base import TestCaseBase
from qrd_shared.case import *
import logging_wrapper

class test_suit_mtsms_case1(TestCaseBase):
    def test_case_main(self, case_results):

        sms_num = SC.PUBLIC_LOCAL_SLOT1_NUMBER
        sms_text=SC.PUBLIC_MESSAGE_CONTENTS
        sms_repeat_times = int(SC.PRIVATE_SMS_REPEAT_NUMBER)
        intervaltime=int(SC.PRIVATE_SMS_INTERVAL)
        
        try:
            set_can_continue()
            
            launcher.launch_from_launcher("settings")
            settings.disable_wifi()
            settings.enableDATA()
            
#            # Delete all threads
#            launcher.launch_from_launcher("mms")
#            click_imageview_by_index(0)
#            sleep(1)
#            delete_all_threads = "Delete all threads"
#            mms.delete_all_threads()
#            
#            launcher.launch_from_launcher("mtservice")
#            mms.mtsms(sms_num,sms_text,sms_repeat_times,intervaltime)
#            t= int(intervaltime)*int(sms_repeat_times)
#            sleep(t)
            
            for i in range(0,sms_repeat_times):
#                mt_trigger_service_sms(msg_title_text, to, interval, time_out, count=1, msg_type=0, wap_url=" ")
                mt_trigger_service_sms(sms_text, sms_num, intervaltime, 15, count=1, msg_type=0, wap_url=" ")
                sleep(intervaltime)
        except Exception as e:
            '''if an exception occurs,we will set the status of this case to fail'''
            #str_context = get_context_info()
            qsst_log_msg('\texception' + '\t' + time.strftime('%X',time.localtime(time.time())))
            log_test_framework('Test','Exception' + str(e))
            save_fail_log()