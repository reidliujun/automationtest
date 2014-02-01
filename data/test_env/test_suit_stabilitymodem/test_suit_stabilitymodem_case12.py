'''
created by L. JUN
06/06/2013
'''
import fs_wrapper
import settings.common as SC
from case_utility import *
from test_case_base import TestCaseBase
from qrd_shared.case import *
import logging_wrapper
import time
'''
Data scenario
'''

class test_suit_stabilitymodem_case12(TestCaseBase):
    def test_case_main(self, case_results):
        mms_num1 = SC.PUBLIC_LOCAL_SLOT1_NUMBER
        mms_text=SC.PUBLIC_MESSAGE_CONTENTS
        address = SC.PRIVATE_BROWSER_ADDRESS_URL
        check_value = SC.PRIVATE_BROWSER_WEB_TITLE_1
        wait_time = 30.0
        call_number = SC.PUBLIC_SLOT1_NUMBER
        call_slot = 0
        call_duration = 10
#        mt_trigger_service_call(to, wait_time, hold_time, interval, num_of_calls=1, count_off=True)
#        mt_trigger_service_call('15900564675', 10, 10, 30, num_of_calls=2, count_off=True)
#        mt_trigger_service_sms(msg_title_text, to, interval, time_out, count=1, msg_type=0, wap_url=" ")
#        mt_trigger_service_sms('ludf134@#$%_343', '15900564675', 30, 15, count=2, msg_type=0, wap_url=" ")
        
        try:
            flag1 = False
            flag2 = False
            if SC.PUBLIC_DSDS:
                launcher.launch_from_launcher("settings")
                settings.disable_wifi()
                settings.enableDATA()
                settings.set_default_data(2)
                sleep(5)
                for i in range(0,20):
                #===================================================================
                # MT MMS, browser and MO CALL
                #===================================================================
                    mt_trigger_service_sms(mms_text, mms_num1, 60, 15, count=1, msg_type=1, wap_url=" ")
                    launcher.launch_from_launcher("browser")
                    flag1 = browser.access_browser(address, check_value, wait_time, True)
                    launcher.launch_from_launcher("phone")
                    flag2 = phone.phone_call(call_number, call_slot, call_duration)
                    sleep(60)
            else:
                qsst_log_msg('test_suit_stabilitymodem_case10 is DSDS test case' + time.strftime('%X',time.localtime(time.time())))

        except Exception as e:
            qsst_log_msg('\texception' + '\t' + time.strftime('%X',time.localtime(time.time())))
            log_test_framework('Test','Exception' + str(e))
            save_fail_log()





