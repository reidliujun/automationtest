import fs_wrapper
import settings.common as SC
from case_utility import *
from test_case_base import TestCaseBase
from qrd_shared.case import *
import logging_wrapper
'''
SMS+Voice
"1. Make a MO SMS and then make a MO call immediately
2. End the call "
by L. Jun 0704/2013
'''

class test_suit_csfb_case4(TestCaseBase):
    def test_case_main(self, case_results):
        sms_num = SC.PUBLIC_SLOT1_NUMBER
        sms_text=SC.PUBLIC_MESSAGE_CONTENTS
        repeat_times = 2
        call_number_slot1 = '10086'
        call_duration = int(SC.PRIVATE_PHONE_CALL_DURATION)
        interval = int(SC.PRIVATE_PHONE_INTERVAL)
        slot = 0
        total_times = 0
        total_success = 0
        for i in range(0, repeat_times):
            flag1 = False

            try:
                set_can_continue()
                total_times = total_times+1
                t=0
                call_delay = 0
#                launcher.launch_from_launcher("mms")
#                flag1 = mms.sms(sms_num, slot, sms_text)
                start_activity('com.android.contacts','.activities.DialtactsActivity')
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
                            call_delay=int(time_start_strlis[2])+int(time_start_strlis[1])*60+int(time_start_strlis[0])*60*60-int(time_ini_strlis[2])-int(time_ini_strlis[1])*60-int(time_ini_strlis[0])*60*60
#                            print call_delay
                            sleep(3)
                            break
                        t = t+1
                sleep(10)
                if search_view_by_id("endButton"):
                    click_button_by_id("endButton")
                    flag2 = True
                else:
                    flag2 = False
            except Exception as e:
                '''if an exception occurs,we will set the status of this case to fail'''
                #str_context = get_context_info()
                qsst_log_msg(str(i+1) + '\texception' + '\t' + time.strftime('%X',time.localtime(time.time())))
                log_test_framework('Test','Exception')
                save_fail_log()
            
            if flag1 & flag2:
                #qsst_log_case_status(logging_wrapper.STATUS_SUCCESS, 'voice call success', logging_wrapper.SEVERITY_HIGH)
                kpi_log_value("csfb","call_delay",call_delay)
                total_success = total_success+1
            else:
                #qsst_log_case_status(logging_wrapper.STATUS_FAILED, 'voice call failed', logging_wrapper.SEVERITY_HIGH)
                kpi_log_value("csfb","call_delay",call_delay)
                qsst_log_msg(str(i+1) + '\tfail' + '\t' + time.strftime('%X',time.localtime(time.time())))
                save_fail_log()
            
            sleep(3)

        qsst_log_msg(str(total_success) + '/' + str(total_times))
        print_report_line("Total:" +str(total_success) + '/' + str(total_times),)