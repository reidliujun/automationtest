## this is case 6.2
import fs_wrapper
from qrd_shared.case import *
from case_utility import *
from utility_wrapper import *
from test_case_base import TestCaseBase
import settings.common as SC
import logging_wrapper

class test_suit_cmcc_case6(TestCaseBase):
    TAG = "test_suit_cmcc_case62"
    def test_case_main(self, case_results):

        total_times = 0
        total_success = 0
        repeat_times=int(SC.PUBLIC_CASE_REPEAT_NUMBER)
        address = 'pan.baidu.com/share/link?shareid=2983063490&uk=674333259'
        sms_num = SC.PUBLIC_SLOT1_NUMBER
        sms_text=SC.PUBLIC_MESSAGE_CONTENTS
        sms_slot = 0
        download_del=True

        for i in range(0, repeat_times):

            try:
                set_can_continue()
                total_times = total_times+1
                
                '''if file exist, delete it first'''
                if download_del :
                    launcher.launch_from_launcher("downloads")
                    while search_text('shoulei', searchFlag=TEXT_CONTAINS):
                        click_checkbox_by_index(0)
                        click_textview_by_index(2)
                
                '''if download fail, continue next loop'''
                if not download(address):
                    qsst_log_msg(str(i+1) + '\tdownload fail' + '\t' + time.strftime('%X',time.localtime(time.time())))
                    save_fail_log()
                    download_del = False
                    continue
                else:
                    download_del = True
            
                launcher.launch_from_launcher("mms")
                flag1 = mms.sms(sms_num, sms_slot, sms_text)
                if flag1 == False:
                    qsst_log_msg(str(i+1) + '\tsms send fail' + '\t' + time.strftime('%X',time.localtime(time.time())))
                    save_fail_log()
            
                launcher.launch_from_launcher("downloads")
                flag2 = check_download()
                if flag2 == False:
                    qsst_log_msg(str(i+1) + '\tdownload fail' + '\t' + time.strftime('%X',time.localtime(time.time())))
                    save_fail_log()
                if flag1 == True and flag2 == True:
                    total_success = total_success+1
            
            except Exception as e:
                '''if an exception occurs,we will set the status of this case to fail'''
                #str_context = get_context_info()
                qsst_log_msg(str(i+1) + '\texception' + '\t' + time.strftime('%X',time.localtime(time.time())))
                log_test_framework('Test','Exception' + str(e))
                save_fail_log()
            
            sleep(3)

        qsst_log_msg(str(total_success) + '/' + str(total_times))
        print_report_line("Total:" +str(total_success) + '/' + str(total_times),)
        
def download(address):
    launcher.launch_from_launcher("browser")
    if search_text(browser.get_value("exit_browser"),isScrollable=0):
        goback()
    sleep(1)
    scroll_to_top()
    click_textview_by_id("url")
    send_key(KEY_DEL)
    entertext_edittext_by_id("url",address)
    click(666,1216)               #click "go" on keyboard
    sleep(20)
    if search_view_by_id("message"):    # if the page has become unresponsive
        click_button_by_id("button2")
    scroll_to_top()
    click(545,655)                #click "download"
    if not SC.PUBLIC_DSDS:
        func =lambda:search_view_by_id("download_settings_title")
        if wait_for_fun(func,True,30):
            click_button_by_id("download_start")
        else:
            '''if not find OK button, continue to next loop'''
            return False
    else:
        send_key(KEY_HOME)
        launcher.launch_from_launcher("downloads")
    
    '''check whether download started'''
    func = lambda:search_text('shoulei', searchFlag=TEXT_CONTAINS)
    if not wait_for_fun(func, True, 20):
        '''download not start successfully'''
        return False
    else:
        return True
def check_download():
    func = lambda:search_text(cmcc.get_value("inprogress"), searchFlag=TEXT_CONTAINS)
    # if not find in progress, download stop
    if wait_for_fun(func, False, 600):
        '''if not find fail info, than success'''
        if not search_text(cmcc.get_value("unsuccessful")):
            #download successful
            return True
        else:
            return False
    else:
        return False