import fs_wrapper
import settings.common as SC
from case_utility import *
from test_case_base import TestCaseBase
from qrd_shared.case import *
import logging_wrapper
import time


class test_suit_lte_case10(TestCaseBase):
    def test_case_main(self, case_results):
        address = SC.PRIVATE_BROWSER_ADDRESS_URL
        check_value = SC.PRIVATE_BROWSER_WEB_TITLE_1
        wait_time = 30.0
        mms_num = SC.PUBLIC_SLOT1_NUMBER
        mms_text = SC.PUBLIC_MESSAGE_CONTENTS
        mms_slot = 0
        mms_attachment = SC.PRIVATE_MTMMS_MTMMS_ATTACHMENT
        local_number = SC.PUBLIC_LOCAL_SLOT1_NUMBER
        web_title_1 = SC.PRIVATE_BROWSER_WEB_TITLE_1
        web_title_2 = SC.PRIVATE_BROWSER_WEB_TITLE_2
        total_success = 0
        total_times = 0
        repeat_times = int(SC.PUBLIC_CASE_REPEAT_NUMBER)
#        repeat_times = 1

        #=======================================================================
        #start initiate 
        #=======================================================================
        launcher.launch_from_launcher("settings")
        settings.disable_wifi()
        settings.enableDATA()
        sleep(5)
        #=======================================================================
        #start test 
        #=======================================================================
        for i in range(0, repeat_times):
            flag1 = False
            flag2 = False            
            try: 
                set_can_continue()
                total_times = total_times+1
                #===================================================================
                # Open a WEB page
                #===================================================================
                launcher.launch_from_launcher("browser")
                flag1 = browser.access_browser(address, check_value, wait_time, True)
                print flag1
                #===================================================================
                # MO MMS
                #===================================================================
                launcher.launch_from_launcher("mms")
                click_imageview_by_index(0)
                sleep(2)
                send_key(KEY_MENU)
                delete_all_threads = mms.get_value("delete_all_threads")
                if wait_for_fun(lambda:search_text(delete_all_threads), True, 3):
                    click_textview_by_text(delete_all_threads)
                    click_button_by_index(1)
                    wait_for_fun(lambda:search_text(mms.get_value("no_conversations")), True, 5)
                else:
                    goback()
                click_imageview_by_id('action_compose_new')
        #        entertext_edittext_by_index(0, mms_num)
                time.sleep(1)
                osInfo = get_platform_info()
                if(osInfo == "Windows" or osInfo == "Linux-PC"):
                    subprocess.Popen(["adb", "shell", "input text " + mms_num])
                elif(osInfo == "Linux-Phone"):
                    os.system("input text " + mms_num)
                
                click_textview_by_desc(mms.get_value("attach"))
                click_textview_by_text(mms.get_value("capture_picture"))
                if search_view_by_id("alertTitle"):
                    click_imageview_by_index(0)
                    click_button_by_id("button_always")
                if search_view_by_id("message"):
                    click_button_by_id("button2")
                camera.get_picture_by_camera()
                entertext_edittext_by_index(1, mms_text)
                click_textview_by_id("send_button_mms")
                #===================================================================
                # MT MMS
                #===================================================================
                launcher.launch_from_launcher("mtservice")
                mms.mtmms(local_number, mms_text, '1', mms_attachment, '60')
                #===================================================================
                # Open two new web pages 
                #===================================================================
                launcher.launch_from_launcher("browser")
                flag2 = browser.browsing(address,wait_time,web_title_1,web_title_2)
                print flag2
                if flag1 & flag2:
                    total_success = total_success+1
                else:
                    qsst_log_msg(str(i+1) + '\tfail' + '\t' + time.strftime('%X',time.localtime(time.time())))
                    save_fail_log()
            except Exception as e:
                '''if an exception occurs,we will set the status of this case to fail'''
                #str_context = get_context_info()
                qsst_log_msg(str(i+1) + '\texception' + '\t' + time.strftime('%X',time.localtime(time.time())))
                log_test_framework('Test','Exception'+str(e))
                save_fail_log()
                
        qsst_log_msg(str(total_success) + '/' + str(total_times))
        print_report_line("Total:" +str(total_success) + '/' + str(total_times),)
            
            