'''
   This Class provide some presettings operation.

   1.Close lockscreen.
   2.Set default IME as google pinyin.
   3.Set default SMS as always ask.


   @author: U{c_chuanc<c_chuanc@qti.qualcomm.com>}
   @version: version 1.0.0
   @requires: python 2.7+
   @license:

   @see: L{TestCaseBase <TestCaseBase>}
   @note:
   @attention:
   @bug:
   @warning:



'''
import fs_wrapper
import settings.common as SC
import time
from qrd_shared.case import *
from case_utility import *
from logging_wrapper import log_test_case, take_screenshot
from test_case_base import TestCaseBase

class test_suit_settings_case1(TestCaseBase):
    '''
    test_suit_settings_case1 is a class for presettings case.

    @see: L{TestCaseBase <TestCaseBase>}
    '''
    def test_case_main(self, case_results):
        '''
        main entry.according to params of config.xml,make the following settings:
       1.Choose default input.
       2.Close lockscreen.
       3.Set default SMS as always ask.
       4.Set default voice as always ask.
       5.Set default IME as google pinyin.
        '''
        try:
            launcher.launch_from_launcher("settings")
            
            #Close lockscreen
            settings.close_lockscreen()
            time.sleep(1)
            
            #Set default SMS & voice as always ask
            if SC.PUBLIC_DSDS:
                settings.set_default_sms(0)
                settings.set_default_voice(0)
                
#            #set default ime -- google pinyin
#            if SC.PUBLIC_GOOGLE_PINYIN:
#                ime.set_default_input_method(ime.get_value("google_pinyin"))
#                start_activity('com.android.browser','.BrowserActivity')
#                browser.pre_check()
#                ime.close_auto_capitalization_google_pinyin()
#                ime.set_google_pinyin_default_input_en()
        except Exception as e:
            '''if an exception occurs,we will set the status of this case to fail'''
            #str_context = get_context_info()
            qsst_log_msg('\texception' + '\t' + time.strftime('%X',time.localtime(time.time())))
            log_test_framework('Test','Exception' + str(e))
            save_fail_log()