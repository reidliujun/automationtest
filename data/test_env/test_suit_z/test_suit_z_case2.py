'''
   this case test local update function.


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
from qrd_shared.case import *
from case_utility import *
from utility_wrapper import *
from logging_wrapper import log_test_case, take_screenshot
from test_case_base import TestCaseBase

class test_suit_z_case2(TestCaseBase):
    '''
    test_suit_settings_case2 is a class for settings case.

    @see: L{TestCaseBase <TestCaseBase>}
    '''
    def test_case_main(self, case_results):
        '''
        main entry.

        @type case_results: tuple
        @param case_results: record some case result information
        '''
        for i in range(0,1):
            try:
                call("test_suit_airplanemode", "test_suit_airplanemode_case3")
            except Exception as e:
                qsst_log_msg(str(i+1) + '\texception' + '\t' + time.strftime('%X',time.localtime(time.time())))
                log_test_framework('Test','Exception')
                save_fail_log()
                
                
#        def_demo_register(self):
#        fun = lambda:search_view_by_id("btn_done")
#        title = 'message'
#    notificationBar.register_NotificationBar_Event('package_name.android.mms', title , fun)
           
        sleep(240)
        print(240)

