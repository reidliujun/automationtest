'''
Control the suits&cases run.

Test_main.py controls the preset cases , test cases.We can use command the test cases random or repeat.
First, it run init_settings(), get preset cases which you choosed.Second,in the init_env(), run the preset cases. Third, in the init_env(), it run the test cases.If you want be random or repeat
the test cases, you can scan in the init_env().

@author: U{zhibinw<zhibinw@qti.qualcomm.com>}
@author: U{c_chuanc<c_chuanc@qti.qualcomm.com>}
@author: U{c_ywan<c_ywan@qti.qualcomm.com>}

@version: version 1.0.0
@requires: python 2.7+
@license: license

@see: L{test main<test_main>}
@note: Because SU.update() method will reload in init_env(), so we must import settings.common as SC after invoking  init_env()
'''

import os
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
if len(sys.argv) >= 2:
    TEST_ENV_DIR = sys.argv[1]#get test_main.py file location
else:
    # get path 'data/test_env_xxx/' from argument 'data/test_env_xxx/test_main.py'
    l = len('test_main.py')
    TEST_ENV_DIR = sys.argv[0][0:-l]
os.chdir(TEST_ENV_DIR)
import settings.update as SU
SU.update()
SU.auto_match_platform()

import fs_wrapper
import random
import traceback
from logging_wrapper import init_logging_file ,log_test_framework,\
    move_crash, clear_crash, init_status, clear_status,get_last_current_time
from utility_wrapper import end_test_runners_accessibility,init_acessibility_socket, set_can_continue
from test_loader import TestLoader
#from case_utility import is_in_reboot_status,register_app_watcher
from case_utility import *
from qrd_shared.launcher.Launcher import Launcher
from test_case_base import TestCaseBase

SUIT_PLUG_IN_FUNCTION_NAME = 'suit_plug_in'
ENV_DY_PATH = 'LD_LIBRARY_PATH'

def init_env(currentTime=1,repeatTime=1):
    '''
    Run preset test cases.  Lead data(SU.update()). You must update the data(SU.update()),before you run the preset test case. Because some preset case will use data which in data(SU.update()).
    '''
    init_logging_file(current_number,global_number,TEST_ENV_DIR)
    #clear the last crash dir
    clear_crash()
    if not init_acessibility_socket():
        return
    if not is_in_reboot_status():
        init_settings()

    #go_back the STK pop dialog
#    register_condition_action_watcher("com.android.stk", VIEW_BUTTON , ID_TYPE_ID, "button_ok", 
#                            ACTION_GO_BACK,VIEW_BUTTON , ID_TYPE_ID, "button_ok")
#    log_test_framework("test_main","stkDialog condition watcher")
#    
#    #class 0 mms 
#    register_condition_action_watcher("com.android.mms", VIEW_BUTTON , ID_TYPE_TEXT, "cancel", 
#                            ACTION_CLICK,VIEW_BUTTON , ID_TYPE_TEXT, "cancel" )
#    log_test_framework("test_main","mms class0 watcher")

    # incomingcall will reject
    #register_app_watcher("incomingcall", VIEW_IMAGE_VIEW , ID_TYPE_ID, "incomingCallWidget", ACTION_LEFT_DRAG )
    #register_condition_action_watcher("phone", VIEW_IMAGE_VIEW , ID_TYPE_ID, "incomingCallWidget", 
    #                        ACTION_LEFT_DRAG ,VIEW_IMAGE_VIEW, ID_TYPE_ID, "incomingCallWidget")
    #log_test_framework("test_main","reject incomingCallWidget watcher")


def init_settings():
    '''
    Load preset test cases. Find test suit which in test_suit_setting.After run preset test case, it will tag the suit False. When run the test case , preset case will not run again.
    '''
    global test_loader
    #TODO: use class to call settings suit
    fs_wrapper.run_init_settings = True
    suit_name = "test_suit_settings"
    suit_py_module_name = "settings.test_suit_settings"
    test_suit = test_loader.loadTestSuitFromName(suit_py_module_name, suit_name)
    suit_results = []
    #call main entry function
    if test_suit != None:
        test_suit.test_suit_run(suit_results)
    fs_wrapper.run_init_settings = False

def end_test():
    '''
    Run test cases. Random or repeat test cases. First, lead test suit list. Second,repeat case 1~x x is be defined on Settings config.Third, random test case if you choose on  Settings config.
    '''
    #move the crash to the current log dir
    move_crash()
    clear_status()
    #back to auto test after end
    set_can_continue()
    launcher = Launcher()
    launcher.launch_from_launcher('auto_test')
    end_test_runners_accessibility()

if __name__ == '__main__':

    #import settings.common as SC
    import settings.common as SC
    # load all test suits and cases
    global test_loader
    test_loader = TestLoader()
    global_number = SC.PUBLIC_RUNNING_REPEAT_NUMBER

    #init the status , include to know whether is it in reboot status
    init_status()
    last_current_time = get_last_current_time()

    for current_number in range(int(last_current_time),int(global_number)):
        TestCaseBase.cycle_index = current_number + 1
        #init the env each report time
        init_env(current_number,global_number)
        log_test_framework("test_main","Current report "+str(current_number)+"/"+str(global_number))
        try:
            if SC.PUBLIC_RANDOM_ORDER:
                # random
                #get the all case list
                case_list = test_loader.getCaseList('./')
                random.shuffle(case_list)
                for case in case_list:
                    try:
                        import qrd_shared.case
                        qrd_shared.case.call(case[0], case[1])
                    except Exception as e:
                        log_test_framework('test_main',"Error :" + str(e))
                        log_test_framework('test_main',"Traceback :" + traceback.format_exc())
            else:
                suit_list = test_loader.loadTestSuit('./')
                if suit_list != None and len(suit_list) > 0:
                    #report suits count
                    log_test_framework('test_main',"All test suites (" + str(len(suit_list)) + ") :")
                    # run all test suits
                    suit_results = []
                    for suit in suit_list:
                        log_test_framework('test_main',"Suite : " + suit.name)
                        try:
                            suit.test_suit_run(suit_results)
                        except Exception as e:
                            log_test_framework('test_main',"Error :" + str(e))
                            log_test_framework('test_main',"Traceback :" + traceback.format_exc())
        except Exception as e:
            log_test_framework('test_main',"Error :" + str(e))
            log_test_framework('test_main',"Traceback :" + traceback.format_exc())

        log_test_framework("test_main","\n all suit finished.")
    end_test()

