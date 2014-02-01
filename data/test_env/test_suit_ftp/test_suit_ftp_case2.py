import fs_wrapper
import settings.common as SC
from case_utility import *
from test_case_base import TestCaseBase
from qrd_shared.case import *
import logging_wrapper
import time
import string

class test_suit_ftp_case2(TestCaseBase):
    
    def test_case_main(self, case_results):

        ftp_address =SC.PRIVATE_FTP_FTP_ADDRESS
        ftp_port = SC.PRIVATE_FTP_FTP_PORT
        ftp_username = SC.PRIVATE_FTP_FTP_USERNAME
        ftp_password = SC.PRIVATE_FTP_FTP_PASSWORD
        download_path = SC.PRIVATE_FTP_FTP_SERVER_DLPATH
        time_expire = int(SC.PRIVATE_FTP_FTP_DOWNLOAD_EXPIRETIME)
        dl_file = SC.PRIVATE_FTP_FTP_DOWNLOAD_FILE
        repeat_times = int(SC.PRIVATE_FTP_FTP_REPEAT_TIMES)
        total_times = 0
        time_after_off = int(SC.PRIVATE_AIRPLANEMODE_TIME_AFTER_MODE_OFF)
        
        try:
            #turn off airplane mode
            launcher.launch_from_launcher("settings")
            settings.disable_wifi()
            settings.enableDATA()
    
            launcher.launch_from_launcher("andftp")
            sleep(2)
            if search_text("Disable tips"):
                click_textview_by_text("Disable tips")
                click_textview_by_text("Close")
            if search_text("59.61"):
                click_button_by_text("Edit")
                entertext_edittext_by_index(5,download_path)
                goback()
                click_textview_by_text("Save")
                click_textview_by_text("Ok")
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
    
            # check log in
            if wait_for_fun(lambda:search_text("100KB.bin"), True, 100):
    
                for i in range(0, repeat_times):
                    total_times = total_times+1
                    click_textview_by_text(dl_file)
                    click_textview_by_text("Download")
                    click_textview_by_text("Ok")
                    time_start=time.strftime('%X',time.localtime(time.time()))
                    t_expire = 0
                    while(1):
                        time.sleep(1)
                        t_expire = t_expire +1
                        if t_expire > time_expire:
                            flag1 = False
                            goback()
                            break
                        if (search_text("Download completed")):
                            click_textview_by_text("Ok")
                            time_end=time.strftime('%X',time.localtime(time.time()))
                            flag1=True
                            break
                        if (search_text("Download failed")):
                            click_textview_by_text("Ok")
                            flag1=False
                            break
    
                    if  flag1==True:
                        time_start_strlis=time_start.split(':')
                        time_end_strlis=time_end.split(':')
                        sec=int(time_end_strlis[2])+int(time_end_strlis[1])*60+int(time_end_strlis[0])*60*60-int(time_start_strlis[2])-int(time_start_strlis[1])*60-int(time_start_strlis[0])*60*60
                        if string.find(dl_file, "KB") != -1:
                            sizestr=dl_file.split("KB")
                            speed=float(sizestr[0])/float(sec)
                            qsst_log_msg("Times:"+str(i+1)+'\t'+str(speed)+"KB/s")
                        elif string.find(dl_file, "MB") !=-1:
                            sizestr=dl_file.split("MB")
                            speed=float(sizestr[0]*1024)/float(sec)
                            qsst_log_msg("Times:"+str(i+1)+'\t'+str(speed)+"KB/s")
                        else:
                            qsst_log_msg("Times:"+str(i+1)+'\t'+'input file name error!')
    
                        case_results.append((self.case_config_map[fs_wrapper.CASE_NAME_ATTR], can_continue()))
                    else:
                        qsst_log_msg(str(i+1) + '\tfail' + '\t' + time.strftime('%X',time.localtime(time.time())))
                        save_fail_log()
                    sleep(5)
            else:
                qsst_log_msg("Log in failed")
    
            click_textview_by_text("Disconnect")
        except Exception as e:
                '''if an exception occurs,we will set the status of this case to fail'''
                #str_context = get_context_info()
                qsst_log_msg(str(i+1) + '\texception' + '\t' + time.strftime('%X',time.localtime(time.time())))
                log_test_framework('Test','Exception' + str(e))
                save_fail_log()
        qsst_log_msg("Total times:"+ str(total_times))