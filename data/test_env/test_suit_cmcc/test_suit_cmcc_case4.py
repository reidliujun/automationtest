''' this is case 5.2
## By L. Jun 15/4/2013'''
import fs_wrapper
from qrd_shared.case import *
from case_utility import *
from utility_wrapper import *
from test_case_base import TestCaseBase
import settings.common as SC
import logging_wrapper

class test_suit_cmcc_case4(TestCaseBase):
    TAG = "test_suit_cmcc_case52"
    def test_case_main(self, case_results):

        total_times = 0
        total_success = 0
        repeat_times=int(SC.PUBLIC_CASE_REPEAT_NUMBER)
        address = SC.PRIVATE_BROWSER_ADDRESS_URL
        wait = float(SC.PRIVATE_BROWSER_WAIT_TIME)
        web_title_1 = unicode(SC.PRIVATE_BROWSER_WEB_TITLE_1)
        web_title_2 = unicode(SC.PRIVATE_BROWSER_WEB_TITLE_2)
        mms_num = SC.PUBLIC_SLOT1_NUMBER
        mms_text = SC.PUBLIC_MESSAGE_CONTENTS
        mms_slot = 0

        for i in range(0, repeat_times):
            
            try:
                set_can_continue()
                total_times = total_times+1
                
                launcher.launch_from_launcher("browser")
                if search_text(browser.get_value("exit_browser"),isScrollable=0):
                    goback()
                flag1 = browser.browsing(address,wait,web_title_1,web_title_2)
                if not flag1:
                    qsst_log_msg(str(i+1) + '\tbrowsing_1 fail' + '\t' + time.strftime('%X',time.localtime(time.time())))
                    continue
                
                launcher.launch_from_launcher("mms")
                flag2 = mms.mms(mms_num, mms_slot, mms_text)
                if not flag2:
                    qsst_log_msg(str(i+1) + '\tmms fail' + '\t' + time.strftime('%X',time.localtime(time.time())))
                    continue
                
                launcher.launch_from_launcher("browser")
                flag3 = browser.browsing(address,wait,web_title_1,web_title_2)
                if not flag3:
                    qsst_log_msg(str(i+1) + '\t browsing_2 fail' + '\t' + time.strftime('%X',time.localtime(time.time())))
                    continue
                
                if flag1 == True and flag2 == True and flag3 == True:
                    total_success = total_success+1

            except Exception as e:
                '''if an exception occurs,we will set the status of this case to fail'''
                #str_context = get_context_info()
                qsst_log_msg(str(i+1) + '\texception' + '\t' + time.strftime('%X',time.localtime(time.time())))
                log_test_framework('Test','Exception' + str(e))
                save_fail_log()
                
            sleep(3)

        qsst_log_msg(str(total_success) + '/' + str(total_times))
        print_report_line("Total:" +str(total_success) + '/' + str(total_times),)