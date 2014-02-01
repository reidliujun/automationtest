import fs_wrapper
from case_utility import *
from qrd_shared.case import *
import settings.common as SC
from test_case_base import TestCaseBase

class test_suit_ss_case10(TestCaseBase):
    def test_case_main(self,case_results):
        
        forward_num = '02120366019'
        repeat_times = int(SC.PUBLIC_CASE_REPEAT_NUMBER)
            
        for i in range(0, repeat_times):
            
            try:
                set_can_continue()
                launcher.launch_from_launcher("phone")
                send_key(KEY_MENU)
                #click_menuitem_by_text(phone.get_value("settings"))
                settings = phone.get_value("settings")
                if search_text(settings):
                    click_textview_by_text(phone.get_value("settings"))
                    #click_button_by_index(0)
                else:
                    goback()
                
                phone.call_forwarding_on(forward_num,3,1)
                sleep(10)
                launcher.launch_from_launcher("phone")
                send_key(KEY_MENU)
                #click_menuitem_by_text(phone.get_value("settings"))
                settings = phone.get_value("settings")
                if search_text(settings):
                    click_textview_by_text(phone.get_value("settings"))
                    #click_button_by_index(0)
                else:
                    goback()
                phone.call_forwarding_off(3,1)
                
            except Exception as e:
                '''if an exception occurs,we will set the status of this case to fail'''
                #str_context = get_context_info()
                qsst_log_msg(str(i+1) + '\texception' + '\t' + time.strftime('%X',time.localtime(time.time())))
                log_test_framework('Test','Exception'+str(e))
                save_fail_log()