import fs_wrapper
import settings.common as SC
from case_utility import *
from test_case_base import TestCaseBase
from qrd_shared.case import *
import logging_wrapper
import time

class test_suit_switchnetwork_case1(TestCaseBase):
    def test_case_main(self, case_results):

        total_times = 0
        time_after_off = int(SC.PRIVATE_AIRPLANEMODE_TIME_AFTER_MODE_OFF)
        repeat_times=int(SC.PRIVATE_SWITCHNETWORK_REPEAT_NUMBER)
        time_after_switch = int(SC.PRIVATE_SWITCHNETWORK_TIME_AFTER_SWITCH)
        
        #turn off airplane mode
        launcher.launch_from_launcher("settings")
        settings.turn_off_airplane(time_after_off)

        for i in range(0, repeat_times):
            total_times = total_times+1
            try:
                set_can_continue()
                launcher.launch_from_launcher("settings")
                settings.switch_network(time_after_switch)
            except Exception as e:
                '''if an exception occurs,we will set the status of this case to fail'''
                #str_context = get_context_info()
                qsst_log_msg(str(i+1) + '\texception' + '\t' + time.strftime('%X',time.localtime(time.time())))
                log_test_framework('Test','Exception' + str(e))
                save_fail_log()
            sleep(3)

        qsst_log_msg('total_times: ' + str(total_times))
        print_report_line('total_times: ' + str(total_times))