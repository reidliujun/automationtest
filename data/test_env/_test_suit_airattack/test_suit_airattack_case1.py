#coding=utf-8
import fs_wrapper
import settings.common as SC
from qrd_shared.case import *
from case_utility import *
from logging_wrapper import log_test_case, take_screenshot
from test_case_base import TestCaseBase
import os


class test_suit_airattack_case1(TestCaseBase):
    def test_case_main(self, case_results):
        sleep(5)
        for i in range(1,100):
            os.system("/system/bin/mysendevent /data/d5")
            sleep(1)
        pass
