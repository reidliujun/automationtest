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

class test_suit_stabilitymodem_case8(TestCaseBase):
    def test_case_main(self, case_results):
        sms_num1 = SC.PUBLIC_LOCAL_SLOT1_NUMBER
        sms_text=SC.PUBLIC_MESSAGE_CONTENTS
#        mt_trigger_service_call(to, wait_time, hold_time, interval, num_of_calls=1, count_off=True)
#        mt_trigger_service_call('15900564675', 10, 10, 30, num_of_calls=2, count_off=True)
#        mt_trigger_service_sms(msg_title_text, to, interval, time_out, count=1, msg_type=0, wap_url=" ")
#        mt_trigger_service_sms('ludf134@#$%_343', '15900564675', 30, 15, count=2, msg_type=0, wap_url=" ")
        
        try:
            launcher.launch_from_launcher("settings")
            settings.disable_wifi()
            settings.enableDATA()
            sleep(5)
            #===============================================================================
            # Long ping 2 hours
            #===============================================================================
            osInfo = get_platform_info()
            if(osInfo == "Windows" or osInfo == "Linux-PC"):
                subprocess.Popen(["adb", "shell", "ping -w 7200 8.8.8.8 &"])
            elif(osInfo == "Linux-Phone"):
                os.system("ping -w 7200 8.8.8.8 &")
                
            for i in range(0,120):
            #===================================================================
            # MT SMS and MT CALL on slot1
            #===================================================================
                mt_trigger_service_sms(sms_text, sms_num1, 60, 15, count=1, msg_type=0, wap_url=" ")
                mt_trigger_service_call(sms_num1, 10, 10, 60, num_of_calls=1, count_off=True)
                sleep(60)

        except Exception as e:
            qsst_log_msg('\texception' + '\t' + time.strftime('%X',time.localtime(time.time())))
            log_test_framework('Test','Exception' + str(e))
            save_fail_log()
        if isAliveforProcess("ping"):
            kill_by_name("ping")
        






