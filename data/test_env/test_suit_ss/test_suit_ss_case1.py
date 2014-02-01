import fs_wrapper
from case_utility import *
from qrd_shared.case import *
import settings.common as SC
from test_case_base import TestCaseBase

class test_suit_ss_case1(TestCaseBase):
    def test_case_main(self,case_results):
        repeat_times = int(SC.PUBLIC_CASE_REPEAT_NUMBER)
        interval = 30
            
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
                phone.call_waiting_on(0)
                launcher.launch_from_launcher("phone")
                send_key(KEY_MENU)
                #click_menuitem_by_text(phone.get_value("settings"))
                settings = phone.get_value("settings")
                if search_text(settings):
                    click_textview_by_text(phone.get_value("settings"))
                    #click_button_by_index(0)
                else:
                    goback()
                phone.call_waiting_off(0)

#                phone.call_waiting(0)
#                phone.call_waiting(1)
#                flag1 = phone.phone_call(call_number_slot1, call_slot, call_duration)
            except Exception as e:
                '''if an exception occurs,we will set the status of this case to fail'''
                #str_context = get_context_info()
                qsst_log_msg(str(i+1) + '\texception' + '\t' + time.strftime('%X',time.localtime(time.time())))
                log_test_framework('Test','Exception'+str(e))
                save_fail_log()
            sleep(interval)