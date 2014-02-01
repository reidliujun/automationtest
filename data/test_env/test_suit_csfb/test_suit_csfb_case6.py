import fs_wrapper
import settings.common as SC
from case_utility import *
from test_case_base import TestCaseBase
from qrd_shared.case import *
import logging_wrapper
'''
MT SMS + DL throughput
"1. Make FTP DL in LTE cell 
2. Make a MT SMS to the DUT"
by L. Jun 0704/2013
'''

class test_suit_csfb_case6(TestCaseBase):
    def test_case_main(self, case_results):
        sms_num = SC.PUBLIC_LOCAL_SLOT1_NUMBER
        sms_text=SC.PUBLIC_MESSAGE_CONTENTS
        repeat_times = int(SC.PUBLIC_CASE_REPEAT_NUMBER)
        intervaltime=SC.PRIVATE_SMS_INTERVAL
        ftp_address =SC.PRIVATE_FTP_FTP_ADDRESS
        ftp_port = SC.PRIVATE_FTP_FTP_PORT
        ftp_username = SC.PRIVATE_FTP_FTP_USERNAME
        ftp_password = SC.PRIVATE_FTP_FTP_PASSWORD
        download_path = SC.PRIVATE_FTP_FTP_SERVER_DLPATH
        dl_file = SC.PRIVATE_FTP_FTP_DOWNLOAD_FILE
        total_success = 0
        total_times = 0
        for i in range(0, repeat_times):
            flag1 = False
            try:
                set_can_continue()
                total_times = total_times+1
                # Delete all threads
                launcher.launch_from_launcher("settings")
                settings.disable_wifi()
                launcher.launch_from_launcher("settings")
                settings.enableDATA()
                
                launcher.launch_from_launcher("mms")
                click_imageview_by_index(0)
                sleep(1)
                delete_all_threads = "Delete all threads"
                mms.delete_all_threads()
                
                launcher.launch_from_launcher("mtservice")
                mms.mtsms(sms_num,sms_text,'1',intervaltime)
                
                launcher.launch_from_launcher("andftp")
                sleep(2)
                if search_text("Disable tips"):
                    click_textview_by_text("Disable tips")
                    click_textview_by_text("Close")
        #        if not search_text("124.127.126.216"):
                if search_text("124.127"):
                    click_textview_by_text("Connect")
                else:
                    click_textview_by_text("Add")
                    sleep(4)
                    entertext_edittext_by_index(0,ftp_address)
                    entertext_edittext_by_index(1,ftp_port)
                    entertext_edittext_by_index(2,ftp_username)
                    entertext_edittext_by_index(3,ftp_password)
                    entertext_edittext_by_index(5,download_path)
                    goback()
                    click_textview_by_text("Save")
                    click_textview_by_text("Ok")
                    click_textview_by_text("Ok")
                    click_textview_by_text("Connect")
                if wait_for_fun(lambda:search_text("100KB.zip"), True, 70):
                    click_textview_by_text(dl_file)
                    click_textview_by_text("Download")
                    click_textview_by_text("Ok")
                    time_start=time.strftime('%X',time.localtime(time.time()))
                    while(1):
                        time.sleep(1)
                        if (search_text("Download completed")):
                            time_end=time.strftime('%X',time.localtime(time.time()))
                            flag1=True
                            break
                        if (search_text("Download failed")):
                            flag1=False
                            break
                    click_textview_by_text("Ok")
                else:
                    flag1 = False
    #            launcher.launch_from_launcher("mms")
    #            click_imageview_by_index(0)
            except Exception as e:
                '''if an exception occurs,we will set the status of this case to fail'''
                #str_context = get_context_info()
                qsst_log_msg('\texception' + '\t' + time.strftime('%X',time.localtime(time.time())))
                log_test_framework('Test','Exception')
                save_fail_log()
            if flag1 :
                #qsst_log_case_status(logging_wrapper.STATUS_SUCCESS, 'voice call success', logging_wrapper.SEVERITY_HIGH)
                #qsst_log_msg(str(i+1) + '\tsuccess' + '\t' + time.strftime('%X',time.localtime(time.time())))
                total_success = total_success+1
            else:
                #qsst_log_case_status(logging_wrapper.STATUS_FAILED, 'voice call failed', logging_wrapper.SEVERITY_HIGH)
                qsst_log_msg(str(i+1) + '\tfail' + '\t' + time.strftime('%X',time.localtime(time.time())))
                save_fail_log()
            
            sleep(3)

        qsst_log_msg(str(total_success) + '/' + str(total_times))
        print_report_line("Total:" +str(total_success) + '/' + str(total_times),)