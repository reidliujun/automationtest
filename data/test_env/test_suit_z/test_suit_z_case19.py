'''
   this class test some behavior of settings.

    1.Enable wifi
    2.Disable wifi
    3.Add a google account
    4.Set default voice as slot1
    5.set default sms as slot1
    6.set two SIM, configure to 2 SIM. 
    7.stream  

   @author: U{c_chuanc<c_chuanc@qti.qualcomm.com>}
   @version: version 1.0.0
   @requires: python 2.7+
   @license:

   @see: L{TestCaseBase <TestCaseBase>}
   @note:
   @attention:
   @bug:
   @warning:



'''
import fs_wrapper
import settings.common as SC
from qrd_shared.case import *
from case_utility import *
from utility_wrapper import *
from logging_wrapper import log_test_case, take_screenshot
from test_case_base import TestCaseBase

class test_suit_z_case19(TestCaseBase):
    '''
    test_suit_z_case1 is a class for concurrency case.

    @see: L{TestCaseBase <TestCaseBase>}
    '''
    def test_case_main(self, case_results):
        '''
        main entry.

        @type case_results: tuple
        @param case_results: record some case result information
        '''
#        count = 0
#        flag = True
#        while(flag):
#            if not settings.enable_wifi(SC.PUBLIC_WIFI_NAME, SC.PUBLIC_WIFI_PASSWORD_SEQUENCE):
#                count += 1
#                if count == 3:
#                    flag = False
#            else:
#                flag = False
#        register_update_watcher(streaming.get_value('youku'), VIEW_BUTTON, ID_TYPE_TEXT, streaming.get_value("retry"), ACTION_CLICK) 
########scenerios10###############################
        print(0)
        launcher.launch_from_launcher('settings')
        settings.enable_wifi(SC.PUBLIC_WIFI_NAME, SC.PUBLIC_WIFI_PASSWORD_SEQUENCE)
        settings.whether_open_gps(True)
        settings.enable_bluetooth()
        #launcher.launch_from_launcher('gtalk')
        #settings.add_google_account(SC.PUBLIC_GMAIL_NAME, SC.PUBLIC_GMAIL_PASSWORD_SEQUENCE)
        #launcher.launch_from_launcher('gtalk')
#        settings.set_default_voice(0)
#        settings.set_default_sms(0)
        print(22)
        #kill_by_name('com.quicinc.fmradio')
        print(33)
        #kill_by_name('gtalk')
        goback()
        sleep(240)
        print(240)
#        if call("test_suit_mtcall", "test_suit_mtcall_case1"):
#            success += 1
#        if call("test_suit_mtcall", "test_suit_mtcall_case2"):
#            success += 1
#        if call("test_suit_weibo", "test_suit_weibo_case1"):
#            success += 1
#        if call("test_suit_gmail", "test_suit_gmail_case3"):
#            success += 1
#        if call("test_suit_email", "test_suit_email_case5"):
#            success += 1
#        if call("test_suit_camera", "test_suit_camera_case7"):
#            success += 1
#        if call("test_suit_camera", "test_suit_camera_case8"):
#            success += 1
        goback()
        sleep(1)
        sleep(1)
        case_results.append((self.case_config_map[fs_wrapper.CASE_NAME_ATTR], can_continue()))
        
        
        
        #sleep(1)
        #scroll_up()
#        click_textview_by_text(settings.get_value("dual_sim_settings"))
#        click_textview_by_text(settings.get_value("configure_subscriptions"))
#        click_checkbox_by_index(1)
#        
        #if getRuntimeEnv() == ROBOTIUM:
        #    switch_socket_by_alias(PHONE)
        #if not is_checkbox_checked_by_index(0):
        #    click_checkbox_by_index(0)
        #click_textview_by_text(settings.get_value("count_down_time"))
        #set_progressbar_by_index(0, "0")
        #click_button_by_index(1)
        #click_textview_by_text(settings.get_value("voice"))
        #click_textview_by_text(settings.get_value("slot2"))
        #click_textview_by_text(settings.get_value("data_call"))
        #click_textview_by_text(settings.get_value("slot2"))
        #sleep(2)
        #click_textview_by_text(settings.get_value("sms"))
        #click_textview_by_text(settings.get_value("slot2"))
        #goback()

        #settings.disable_wifi()
        #settings.whether_open_gps(False)
        #sleep(5)
        case_results.append((self.case_config_map[fs_wrapper.CASE_NAME_ATTR], can_continue()))

