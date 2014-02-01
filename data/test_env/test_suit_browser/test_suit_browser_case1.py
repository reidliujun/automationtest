#coding=utf-8
import fs_wrapper
import settings.common as SC
from case_utility import *
from test_case_base import TestCaseBase
import logging_wrapper
from qrd_shared.case import *
import time

class test_suit_browser_case1(TestCaseBase):
    def test_case_main(self, case_results):

        total_times = 0
        total_success = 0
        address = SC.PRIVATE_BROWSER_ADDRESS_URL
        repeat_times = int(SC.PRIVATE_BROWSER_REPEAT_NUMBER)
        wait = float(SC.PRIVATE_BROWSER_WAIT_TIME)
        web_title_1 = SC.PRIVATE_BROWSER_WEB_TITLE_1
        web_title_2 = SC.PRIVATE_BROWSER_WEB_TITLE_2
        time_after_off = int(SC.PRIVATE_AIRPLANEMODE_TIME_AFTER_MODE_OFF)
        
        #turn off the wifi
        launcher.launch_from_launcher("settings")
        settings.disable_wifi()
        settings.turn_off_airplane(time_after_off)

        if SC.PUBLIC_DSDS:
            #switch data call to slot 1
            launcher.launch_from_launcher("settings")
            settings.set_default_data(1)
        
        for i in range(0, repeat_times):
            flag1 = False
            
            try:
                set_can_continue()
                total_times = total_times+1
                
                launcher.launch_from_launcher("browser")
                flag1 = browser.browsing(address,wait,web_title_1,web_title_2)
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