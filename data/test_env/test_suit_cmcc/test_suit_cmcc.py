from utility_wrapper import *
import fs_wrapper
from logging_wrapper import log_test_suit
from test_suit_base import TestSuitBase

CASE_PLUG_IN_FUNCTION_NAME = 'case_plug_in'
test_suit_config_map = {}
global_suit_config_map = {}

class test_suit_cmcc(TestSuitBase):
    def test_suit_init_robotium(self):
        kill_by_name("com.android.settings")
        return True