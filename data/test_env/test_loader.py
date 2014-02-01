'''
   test loader for qsst python framework

   This module used to provide utilities for loading the suits or cases from the qsst framework,
   such as: load test suit from name ; dump test suit; get case list and so on

   If you want to add some common function to load suit or case,
   you can also added them here.


   @author: U{c_lqiang<c_lqiang@qti.qualcomm.com>}
   @version: version 1.0.0
   @requires:python 2.7+
   @license:

   @see: L{test_case_base<test_case_base>}
   @note:
   @attention:
   @bug:
   @warning:


'''
import os
import fs_wrapper
import case_utility
from test_suit_base import TestSuitBase
from test_case_base import TestCaseBase
from logging_wrapper import log_test_framework, is_suit_in_reboot_status,\
    is_in_reboot_status, is_case_in_reboot_status, get_reboot_reason,\
    REBOOT_CRASH, qsst_log_restore_reboot
TAG = 'TestLoader'
class TestLoader(object):
    ''' load case or suit'''
    def __init__(self):
        pass

    def loadTestSuitFromName(self, suit_module_name, suit_name):
        '''
        load test suit from name

        @type suit_module_name: string
        @param suit_module_name: suit module name
        @type suit_name: string
        @param suit_name: suit name
        @return: return the suit instance
        '''
        suit_config_map = fs_wrapper.get_test_suit_config(suit_name)
        if suit_config_map.get(fs_wrapper.SUIT_ENABLE_ATTR) != '1':
            return None
        suit_info = None

        # create test suit instance
        test_suit = TestSuitBase.createInstance(suit_module_name + fs_wrapper.DOT_TAG + suit_name, suit_name, suit_info)
        if suit_config_map.get(fs_wrapper.SUIT_RUNNER_ATTR) != None:
            test_suit.runner = suit_config_map.get(fs_wrapper.SUIT_RUNNER_ATTR)
        if suit_config_map.get(fs_wrapper.SUIT_APP_NAME) != None:
            app_name =  suit_config_map.get(fs_wrapper.SUIT_APP_NAME)


        # load test cases for test suit.
        # It will aggregate all the relative suit info for this test suit, too.
        cases = fs_wrapper.get_all_cases_py_module_name(test_suit.name)
        #relative_suits = []
        status = 0
        if is_suit_in_reboot_status(suit_name) and is_in_reboot_status():
            status = 1
        log_test_framework(TAG, "suit_name:"+suit_name)
        for case in cases:
            log_test_framework(TAG, "check case:"+case[1])
            if status == 1 and not is_case_in_reboot_status(case[1]):
                log_test_framework(TAG,  "status == 1 and not is_case_in_reboot_status")
                continue
            elif status == 1 and is_case_in_reboot_status(case[1]):
                log_test_framework(TAG,  "status == 1 and is_case_in_reboot_status")
                status = 2
                if get_reboot_reason() == REBOOT_CRASH:
                    log_test_framework(TAG,  "get_reboot_reason() == REBOOT_CRASH")
                    qsst_log_restore_reboot()
                    continue
                qsst_log_restore_reboot()
            log_test_framework(TAG,  "add case:"+case[1])
            case_config_map = fs_wrapper.get_test_case_config(case[1], test_suit.name)
            if case_config_map.get(fs_wrapper.CASE_ENABLE_ATTR) == '1':
                case_app_name = case_config_map.get(fs_wrapper.CASE_APP_NAME)
                if case_app_name == None or case_app_name == "":
                    case_app_name = app_name
                else:
                    log_test_framework(TAG,'case_app_name null')
                reference = case_config_map.get(fs_wrapper.CASE_REFERENCE);
                if reference != None and reference!= "":
                    (suit_name, case_name) = reference.rsplit('.', 1)
                    class_name = reference + fs_wrapper.DOT_TAG + case_name
                    self.addTestCase(test_suit,case_config_map,class_name, suit_name,case_name, case_app_name)
                else:
                    self.addTestCase(test_suit,case_config_map,case[0] + fs_wrapper.DOT_TAG + case[1], suit_name,case[1], case_app_name)
        return test_suit

    def addTestCase(self, test_suit, caseConfigMap, className, suitName, caseName, appName):
        '''
        add the case to the suit

        @type test_suit: L{TestSuitBase<TestSuitBase>}
        @param test_suit: suit you want to operation
        @type caseConfigMap: array
        @param caseConfigMap: the configuration map of the case which is adding to the suit
        '''
        test_case = TestCaseBase.createInstance(className, caseName, suitName, appName)
        test_case.case_config_map = caseConfigMap
        log_test_framework(test_case.name, "case added")
        test_suit.addCase(test_case)

    def loadTestSuit(self, base_path):
        '''
        load the test suits from the path

        @type base_path: string
        @param base_path: the path of the suit
        @return: return all the suits which can found under this path
        '''

        # load enabled suit as a list
        suit_names = fs_wrapper.get_suit_name_list(base_path)
        suit_list = []
        status = 0
        if case_utility.is_in_reboot_status():
            status = 1
        for suit_name in suit_names:
            log_test_framework(TAG, "loadTestSuit suit_name:"+suit_name)
            if status == 1 and not case_utility.is_suit_in_reboot_status(suit_name):
                log_test_framework(TAG, "loadTestSuit in not reboot status")
                continue
            elif status == 1 and case_utility.is_suit_in_reboot_status(suit_name):
                log_test_framework(TAG, "loadTestSuit in reboot status")
                status = 2
            suit_py_module_name = fs_wrapper.get_suit_py_module_name(suit_name)
            if len(suit_py_module_name) == 0:
                continue
            # load test suit one by one
            test_suit = self.loadTestSuitFromName(suit_py_module_name, suit_name)
            if test_suit != None:
                log_test_framework(test_suit.name, "suit added")
                suit_list.append(test_suit)

        return suit_list

    def dumpTestSuit(self, suit_list):
        '''
        sump the suit information

        @type suit_list: array
        @param suit_list: the suit list which want to dump
        '''
        for suit in suit_list:
            print str(suit)

    def getCaseList(self, base_path):
        '''
        load the test cases from the path

        @type base_path: string
        @param base_path: the path of the case
        @return: return all the cases which can found under this path
        '''
        all_case_name_list = []
        suit_name_list = fs_wrapper.get_suit_name_list(base_path)
        for suit_name in suit_name_list:
            suit_config_map = fs_wrapper.get_test_suit_config(suit_name)
            if suit_config_map.get(fs_wrapper.SUIT_ENABLE_ATTR) == '1':
                cases = fs_wrapper.get_all_cases_py_module_name(suit_name)
                case_name_list = []
                for case in cases:
                    case_name_list.append(case[1])
                    for case_name in case_name_list:
                        case_config_map = fs_wrapper.get_test_case_config(case_name, suit_name)
                        if case_config_map.get(fs_wrapper.CASE_ENABLE_ATTR) == '1':
                            all_case_name_list.append((suit_name, case_name))
        return all_case_name_list