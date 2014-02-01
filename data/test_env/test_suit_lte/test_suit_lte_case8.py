import fs_wrapper
import settings.common as SC
from case_utility import *
from test_case_base import TestCaseBase
from qrd_shared.case import *
import logging_wrapper
import time
'''
Procedure:
"(1) UE is located in the overlapped coverage of TD-LTE and GSM networks;
(2) Find out one good signal point satisfying TD-LTE network;
(3) UE keeps ftp UL/DL in LTE Cell
(4) Establish MT SMS to the UE.(Please annotate the QXDM log with ""MT SMS Now""."
'''

class test_suit_lte_case8(TestCaseBase):
    def test_case_main(self, case_results):
        
        test_repeat_times = SC.PUBLIC_CASE_REPEAT_NUMBER
        intervaltime = "20"
        sms_num = SC.PUBLIC_LOCAL_SLOT1_NUMBER
        sms_text=SC.PUBLIC_MESSAGE_CONTENTS
        sleeptime = 20 * int(test_repeat_times)
        total_times = 0
        
        address = "http://pan.baidu.com/share/link?shareid=1973012842&uk=1879265910"
        #Initiate
        launcher.launch_from_launcher("settings")
        settings.disable_wifi()
        settings.enableDATA()
        launcher.launch_from_launcher("downloads")
        if search_text("testdownload"):
            click_checkbox_by_index(0)
            click_textview_by_index(2)
        '''
        Start download
        '''
        launcher.launch_from_launcher("browser")
        #addressing config web address
        click_textview_by_id("url")
        send_key(KEY_DEL)
        #input address url
        entertext_edittext_by_id("url",address)
        #ime.IME_input(1,SC.PRIVATE_BROWSER_ADDRESS_URL_SEQUENCE)
        click(670,1230)
        sleep(15)
        click(520,660)
        sleep(10)
        click_button_by_id("download_start")
        
        
        try:
            set_can_continue()
            total_times = total_times+1
            launcher.launch_from_launcher("mtservice")
            mms.mtsms(sms_num,sms_text,test_repeat_times,intervaltime)
            launcher.launch_from_launcher("downloads")
            if search_text("testdownload"):
                click_checkbox_by_index(0)
                sleep(sleeptime)
                click_textview_by_index(2)
            else:
                qsst_log_msg('\tdownload fail' + '\t' + time.strftime('%X',time.localtime(time.time())))
        except Exception as e:
            '''if an exception occurs,we will set the status of this case to fail'''
            #str_context = get_context_info()
            qsst_log_msg('\texception' + '\t' + time.strftime('%X',time.localtime(time.time())))
            log_test_framework('Test','Exception'+str(e))
            save_fail_log()
        
            
            
            
            