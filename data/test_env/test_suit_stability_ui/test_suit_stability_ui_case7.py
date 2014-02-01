import fs_wrapper
import settings.common as SC
from qrd_shared.case import *
from case_utility import *
from test_case_base import TestCaseBase
import time
import logging_wrapper

class test_suit_stability_ui_case7(TestCaseBase):
    def test_case_main(self, case_results):

        repeat_times = int(SC.PUBLIC_CASE_REPEAT_NUMBER)
        call_number_slot1 = SC.PUBLIC_SLOT1_NUMBER
        slot = 0
        call_duration = int('1')
        total_times = 0
        total_success = 0
        
        for i in range(0, repeat_times):
            flag1 = False
            
            try:
                set_can_continue()
                total_times = total_times+1
                #Delete existing contact
                launcher.launch_from_launcher("people")
                contact.del_contact_all()
                
                #Make a MO call
                launcher.launch_from_launcher("phone")
                flag1 = phone.phone_call(call_number_slot1, slot, call_duration)
                
                launcher.launch_from_launcher("phone")
                drag_by_param(0,50,100,50,10)
                drag_by_param(0,50,100,50,10)
                drag_by_param(90,50,10,50,10)
                
                #Choose a number
                click_textview_by_text('10086' or 'test')
                
                #Add new contact
                click_textview_by_id('main_action')
                click_textview_by_id('new_contact')
                entertext_edittext_by_index("0",'test' + str(i+1))
                click_imageview_by_id('icon')
                click_imageview_by_id('home')
                time.sleep(2)
                if search_text('test' + str(i+1), searchFlag=TEXT_CONTAINS):
                    flag1 = True
                else:
                    flag1 = False
            except Exception as e:
                '''if an exception occurs,we will set the status of this case to fail'''
                #str_context = get_context_info()
                qsst_log_msg(str(i+1) + '\texception' + '\t' + time.strftime('%X',time.localtime(time.time())))
                log_test_framework('Test','Exception' + str(e))
                save_fail_log()
            
            if flag1:
                #qsst_log_case_status(logging_wrapper.STATUS_SUCCESS, 'voice call success', logging_wrapper.SEVERITY_HIGH)
                total_success = total_success+1
            else:
                #qsst_log_case_status(logging_wrapper.STATUS_FAILED, 'voice call failed', logging_wrapper.SEVERITY_HIGH)
                qsst_log_msg(str(i+1) + '\tfail' + '\t' + time.strftime('%X',time.localtime(time.time())))
                save_fail_log()
            sleep(3)

        qsst_log_msg(str(total_success) + '/' + str(total_times))
        print_report_line("Total:" +str(total_success) + '/' + str(total_times),)