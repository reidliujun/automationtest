'''
   Base class of all case.

   This module defines the life cycle of test case .
   and makes the case subclass just need to care about the test functions.

   1.test_case_run() function is the entry which the test suit will call it .
   In this function , it will call test_case_init() to init some information about this case.
   then, test_case_main() function will be called, and subclasses just need to override it,and do itself things.
   last, test_case_end() function will be called, and execute to exit this application.

   2.in addition, exit_app() function is used to exit the application after this case is ending.
   it usually call the launcher.back_to_launcher() to exit.
   of course, subclass also can override it and complete itself steps to exit the application.

   3.If you want to add some common function for all the test case ,
   you can add them here.

   @author: U{c_lqiang<c_lqiang@qti.qualcomm.com>}
   @version: version 1.0.0
   @requires:python 2.7+
   @license:

   @see: L{test_suit_base<test_suit_base>}
   @note:
   @attention:
   @bug:
   @warning:



'''
import signal
import fs_wrapper
import traceback
from utility_wrapper import set_can_continue,getprop_suspend,OnshakeSignal_handler
from logging_wrapper import log_test_framework, set_cur_case_name, clear_logcat, save_fail_log,\
    qsst_log_case_init, qsst_log_case_status, get_context_info,log_test_case
from qrd_shared.launcher.Launcher import Launcher
import logging_wrapper
import case_utility

class TestCaseBase(object):
    """Base class for test case"""
    global launcher
    '''cycle index of repeat case'''
    cycle_index = 1
    def __init__(self, name, suit_name, app_name, enabled=True):
        self.name = name
        self.suit_name = suit_name
        self.app_name = app_name
        self.enabled = enabled
        self.launcher = Launcher()

    def test_case_init(self):
        '''
        init the test case . such as: set the L{current_case_continue_flag<current_case_continue_flag>} to True;
        save the current case name; init the logging; launcher this application
        '''
        if getprop_suspend() :
            signal.signal(signal.SIGUSR1, OnshakeSignal_handler)
            log_test_case('suspend', 'suspended, wait for shake-signal from java resume --- 3')
            signal.pause()
            log_test_case('Finally!!!', 'good luck, already gotten signal and resumed.... --- 4')
        log_test_framework(self.name, 'case init...')
        set_can_continue()
        set_cur_case_name(self.name)
        qsst_log_case_init()
        self.launcher.launch_from_launcher(self.app_name)
        clear_logcat()

    def test_case_end(self):
        '''
        end the test case . call L{exit_app<exit_app>} to exit the application
        '''
        self.exit_app()
        log_test_framework(self.name, 'case end')

    def test_case_run(self, case_results):
        '''
        the entry of the case.through this method to control the case life cycle.

        @type case_results: array
        @param case_results: the case result array.
        '''
        try:
            import settings.common as SC
            if fs_wrapper.run_init_settings:
                case_utility.update_notificationbar('presettings is running...')
            else:
                case_utility.update_notificationbar('(' + str(self.cycle_index) +'/' + str(SC.PUBLIC_RUNNING_REPEAT_NUMBER) + ')' + self.suit_name + '.' + self.name)
            self.test_case_init()
            '''init the case'''
        except Exception as e:
            '''if an exception occurs,we will set the status of this case to STATUS_FAILED'''
            self.dealwith_exception(e)
            qsst_log_case_status(logging_wrapper.STATUS_FAILED, str(e), logging_wrapper.SEVERITY_HIGH)
            self.test_case_end()
            return False
        try:
            success = self.test_case_main(case_results)
        except Exception as e:
            '''if an exception occurs,we will set the status of this case to STATUS_FAILED'''
            str_context = get_context_info()

            if str_context == None:
                str_exception = "CONTEXT:"+str_context+" "+logging_wrapper.DIVIDE+str(e)
            else:
                str_exception = str(e)
            qsst_log_case_status(logging_wrapper.STATUS_FAILED, str_exception, logging_wrapper.SEVERITY_HIGH)
            self.dealwith_exception(e)
            self.test_case_end()
            return False
        self.test_case_end()
        if success == None:
            return True
        return success


    def test_case_main(self, case_results):
        '''
        the subclass need to override this function to do itself things

        @type case_results: array
        @param case_results: the case result array.
        '''
        case_results.append((self.name, False))

    def __str__(self):
        return '[Case][Name: %s, SuitName: %s, enabled: %d]' % (self.name, self.suit_name, self.enabled)

    @staticmethod
    def createInstance(class_name, *args, **kwargs):
        '''
        give the class name and the args to create a test instance

        @type class_name: string
        @param class_name: class name of this case
        @type args: reference
        @param args: arguments the case needs
        '''
        (module_name, class_name) = class_name.rsplit('.', 1)
        module_meta = __import__(module_name, globals(), locals(), [class_name])
        class_meta = getattr(module_meta, class_name)
        o = class_meta(*args, **kwargs)
        return o

    # exit the app , the default behavior is to click the back key
    # if your app is not fit , please override this method
    def exit_app(self):
        '''
        exit this application. the subclass can override to complete itself steps to exit it own application
        '''
        try:
            self.launcher.back_to_launcher()
            return True
        except Exception as e:
            self.dealwith_exception(e)
            return False

    def dealwith_exception(self, e):
        '''
        deal with the exception.such as: save the exception stack or exception message
        '''
        save_fail_log()
        log_test_framework('TestCaseBase','Exception is :' + str(e))
        log_test_framework('TestCaseBase','Traceback :' + traceback.format_exc())
