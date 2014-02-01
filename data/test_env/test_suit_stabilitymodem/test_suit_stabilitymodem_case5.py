'''
Modem scenarios test case 26--case 29
created by L. JUN
03/06/2013
'''
import fs_wrapper
import settings.common as SC
from case_utility import *
from test_case_base import TestCaseBase
from qrd_shared.case import *
import logging_wrapper
import time


class test_suit_stabilitymodem_case5(TestCaseBase):
    def test_case_main(self, case_results):
        dsds_flag = SC.PUBLIC_DSDS
        repeat_time = 20
        call_duration = 900 #1200
        total_times = 0
        total_success = 0
        sms_num_slot1 = SC.PUBLIC_LOCAL_SLOT1_NUMBER#"18602114924"
        sms_num_slot2 = SC.PUBLIC_LOCAL_SLOT2_NUMBER#"18602114924"
        sms_text=SC.PUBLIC_MESSAGE_CONTENTS
        interval=30
        
        for i in range(0,repeat_time):
            total_times = total_times+1
            flag1 = False
            flag2 = False
#            launcher.launch_from_launcher("settings")
#            settings.enableDATA()
            osInfo = get_platform_info()
            if(osInfo == "Windows" or osInfo == "Linux-PC"):
                subprocess.Popen(["adb", "shell", "ping -s 500 8.8.8.8 &"])
            elif(osInfo == "Linux-Phone"):
                os.system("ping -s 500 8.8.8.8 &")
            ''' 
                if dual card, call on slot2.
            '''
            if dsds_flag == False:
                call_number_slot = SC.PUBLIC_SLOT1_NUMBER
                call_slot = 0
            else:
                call_number_slot = SC.PUBLIC_SLOT2_NUMBER
                call_slot = 1
            
            try:
                ''' MO Call'''
                set_can_continue()
                launcher.launch_from_launcher("phone")
                flag1 = phone.phone_call(call_number_slot, call_slot, call_duration)
                
                '''MT SMS on Slot1'''
                set_can_continue()
                # Delete all threads
                launcher.launch_from_launcher("mms")
                click_imageview_by_index(0)
                sleep(1)
                delete_all_threads = "Delete all threads"
                mms.delete_all_threads()
                
                launcher.launch_from_launcher("mtservice")
                mms.mtsms(sms_num_slot1,sms_text,1,30)
                
                launcher.launch_from_launcher("mms")
                click_imageview_by_index(0)
                if dsds_flag == True:
                    sleep(interval)
                    '''MT SMS on Slot2'''
                    set_can_continue()
                    # Delete all threads
                    launcher.launch_from_launcher("mms")
                    click_imageview_by_index(0)
                    sleep(1)
                    delete_all_threads = "Delete all threads"
                    mms.delete_all_threads()
                    
                    launcher.launch_from_launcher("mtservice")
                    mms.mtsms(sms_num_slot2,sms_text,1,30)
                    
                    launcher.launch_from_launcher("mms")
                    click_imageview_by_index(0)
                
            except Exception as e:
                '''if an exception occurs,we will set the status of this case to fail'''
                #str_context = get_context_info()
                qsst_log_msg(str(i+1) + '\texception' + '\t' + time.strftime('%X',time.localtime(time.time())))
                log_test_framework('Test','Exception' + str(e))
                save_fail_log()
                #return
            
            if flag1:
                #qsst_log_case_status(logging_wrapper.STATUS_SUCCESS, 'voice call success', logging_wrapper.SEVERITY_HIGH)
                #qsst_log_msg(str(i+1) + '\tsuccess' + '\t' + time.strftime('%X',time.localtime(time.time())))
                total_success = total_success+1
            else:
                #qsst_log_case_status(logging_wrapper.STATUS_FAILED, 'voice call failed', logging_wrapper.SEVERITY_HIGH)
                qsst_log_msg(str(i+1) + '\tfail' + '\t' + time.strftime('%X',time.localtime(time.time())))
                save_fail_log()
            
            sleep(interval)

        qsst_log_msg(str(total_success) + '/' + str(total_times))
        print_report_line("Total:" +str(total_success) + '/' + str(total_times),)