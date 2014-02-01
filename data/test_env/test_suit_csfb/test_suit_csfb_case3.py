import fs_wrapper
import settings.common as SC
from case_utility import *
from test_case_base import TestCaseBase
from qrd_shared.case import *
import logging_wrapper
'''
Voice call+MMS
"1. Make a MO voice call
2. Send a MMS during the voice call
3. End the call after the MMS is sent "
by L. Jun 0704/2013
'''

class test_suit_csfb_case3(TestCaseBase):
    def test_case_main(self, case_results):
        call_number_slot1 = "02161037640"
        repeat_times = int(SC.PUBLIC_CASE_REPEAT_NUMBER)
        call_duration = int(SC.PRIVATE_PHONE_CALL_DURATION)
        interval = int(SC.PRIVATE_PHONE_INTERVAL)
        mms_num = SC.PUBLIC_SLOT1_NUMBER
        mms_text = SC.PUBLIC_MESSAGE_CONTENTS
        mms_slot = 0
        call_slot = 0
        total_times = 0
        total_success = 0

        for i in range(0,repeat_times):
            flag1 = False
            flag2 = False
            
            try:
                set_can_continue()
                total_times = total_times+1
                t=0
                call_delay = 0
                #initiate a mo call
                launcher.launch_from_launcher("phone")
                numberlist = phone.predefined_numbers
                drag_by_param(0,50,100,50,10)
                drag_by_param(0,50,100,50,10)
                #clear existing number
                click_imageview_by_id("deleteButton",clickType=LONG_CLICK)
                call_number_str = [s for s in call_number_slot1 ]
                for callnumber in call_number_str:
                    click_imageview_by_id(numberlist[callnumber])
                click_imageview_by_id("dialButton")
                call_ini_time=time.strftime('%X',time.localtime(time.time()))
                sleep(1)
                while search_view_by_id("endButton") and t < 20:
                        if search_text("0:"):
                            call_start_time=time.strftime('%X',time.localtime(time.time()))
                            time_start_strlis=call_start_time.split(':')
#                            print time_end_strlis
                            time_ini_strlis=call_ini_time.split(':')
#                            print time_start_strlis
                            call_delay = int(time_start_strlis[2])+int(time_start_strlis[1])*60+int(time_start_strlis[0])*60*60-int(time_ini_strlis[2])-int(time_ini_strlis[1])*60-int(time_ini_strlis[0])*60*60
#                            print call_delay
                            sleep(3)
                            break
                        t = t+1
                launcher.launch_from_launcher("mms")
                flag1 = mms.mms(mms_num, mms_slot, mms_text)
                launcher.launch_from_launcher("phone")
                drag_by_param(0,50,100,50,10)
                drag_by_param(0,50,100,50,10)
                if search_text(phone.get_value("return_to_call")):
                    click_textview_by_text(phone.get_value("return_to_call"))
                    if search_view_by_id("endButton"):
                        click_button_by_id("endButton")
                        flag2 = True
                    else:
                        flag2 = False
                else:
                    flag2 = False
            except Exception as e:
                '''if an exception occurs,we will set the status of this case to fail'''
                #str_context = get_context_info()
                qsst_log_msg(str(i+1) + '\texception' + '\t' + time.strftime('%X',time.localtime(time.time())))
                log_test_framework('Test','Exception')
                save_fail_log()
                #return

            if flag1 & flag2:
                #qsst_log_case_status(logging_wrapper.STATUS_SUCCESS, 'voice call success', logging_wrapper.SEVERITY_HIGH)
                #qsst_log_msg(str(i+1) + '\tsuccess' + '\t' + time.strftime('%X',time.localtime(time.time())))
                kpi_log_value("csfb","csfb_case2_call_delay",call_delay)
#                qsst_log_msg('call delay for csfb is:'+' '+call_delay+ 's')
                total_success = total_success+1
            else:
                #qsst_log_case_status(logging_wrapper.STATUS_FAILED, 'voice call failed', logging_wrapper.SEVERITY_HIGH)
                kpi_log_value("csfb","csfb_case2_call_delay",call_delay)
                qsst_log_msg(str(i+1) + '\tfail' + '\t' + time.strftime('%X',time.localtime(time.time())))
                save_fail_log()
            
            sleep(interval)

        qsst_log_msg(str(total_success) + '/' + str(total_times))
        print_report_line("Total:" +str(total_success) + '/' + str(total_times),)