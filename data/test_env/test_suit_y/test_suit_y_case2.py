import fs_wrapper
import settings.common as SC
from qrd_shared.case import *
from case_utility import *
from utility_wrapper import *
from logging_wrapper import log_test_case, take_screenshot
from test_case_base import TestCaseBase

class test_suit_y_case2(TestCaseBase):
    '''
    test_suit_y_case1 is a class for concurrency case.

    @see: L{TestCaseBase <TestCaseBase>}
    '''
    def test_case_main(self, case_results):
        '''
        main entry.

        @type case_results: tuple
        @param case_results: record some case result information
        '''
#
        success = 0
        if call("test_suit_phone", "test_suit_phone_case1"):
            success += 1
        if SC.PUBLIC_DSDS:
            if call("test_suit_phone", "test_suit_phone_case2"):
                success += 1
        goback()
        sleep(1)
#        notificationBar.clear_all()
        if success < 1:
            set_cannot_continue()
        sleep(1)
        case_results.append((self.case_config_map[fs_wrapper.CASE_NAME_ATTR], can_continue()))

