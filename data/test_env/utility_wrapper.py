'''
   utility for qsst python framework

   This module used to provide utilities for qsst python framework,
   support low level operations as initial socket connection, generate
   command line to communicate with server, interact with server and
   so on.

   you can use all the interface in qsst python framework, but not for
   cases. If you want to add some common function utils for framework ,
   you can also added them here.


   @author: U{zhibinw<zhibinw@qti.qualcomm.com>}
   @version: version 1.0.0
   @requires:python 2.7+
   @license:
'''

from io_wrapper import SocketUtil
from exception import SocketException,AssertFailedException
import sys
import os
import time
import subprocess
import signal
import thread
import fs_wrapper
from logging_wrapper import *
from platform_check import get_platform_info


'''tags used for request'''
SEPERATOR = "&sp;"
ACTION_TAG = "action="
DEST_VIEW_TYPE_TAG = "dest_view_type="
DEST_VIEW_ID_TYPE_TAG = "dest_view_id_type="
DEST_VIEW_ID_TAG = "dest_view_id="
VALUE_TAG = "value="
LENGTH_TAG = "len="

ACTION_END = '0'

'''tags used for response'''
STATUS_END = '-1'
STATUS_ACTION_NOT_SUPPORT = '0'
STATUS_OK_WITHOUT_RESULT = '1'
STATUS_OK_WITH_RESULT = '2'
STATUS_ASSERT_FAILED = '3'

SPACE = ' '
LOG_TAG = 'utility_wrapper'

#current socket that's being used
my_socket = None
my_socket_qsst = None
#if assert failes during one case or not, why used this ?
current_case_continue_flag = True

def assert_type_string(i):
    '''
    check whether the input parameter  is a string.
    set L{current_case_continue_flag<current_case_continue_flag>}
    to false if fails.

    @type i: string
    @param i: the parameter to be checked.

    @todo: should raise an exception, not set flag.
    '''
    if not type(i) in [type(''), type(u'')]:
        log_test_framework(LOG_TAG, "parameter invalid")
        current_case_continue_flag = False

def assert_type_int(i):
    '''
    check whether the input parameter is an integer.
    set L{current_case_continue_flag<current_case_continue_flag>}
    to false if fails.

    @type i: int
    @param i: the parameter to be checked.

    @todo: should raise an exception, not set flag.
    '''
    if not type(i) in [type(0)]:
        log_test_framework(LOG_TAG, "parameter invalid")
        current_case_continue_flag = False

#send msg to server and get response
def interact_with_server(cmd):
    '''
    send request command line to server and get response
    line from server.The format of request and response should
    match with server side, so if you want to make any change please
    get familiar with the format of request and responses.

    @type cmd: string
    @param cmd: request command line.
    @todo: should not use contiue flag, use exceptions.
    '''
    if not can_continue():
        return

    global current_case_continue_flag
    log_test_framework(LOG_TAG, 'send: ' + cmd)
    send_result = my_socket.send_msg_line(cmd)
    if not send_result:
        current_case_continue_flag = False
        raise SocketException('send message failed')
    response = ['']
    recv_result = my_socket.get_response_line(response)
    if not recv_result:
        current_case_continue_flag = False
        raise SocketException('receive message failed')
    response_line = response[0]
    log_test_framework(LOG_TAG, 'receive: ' + response_line)
    if response_line.startswith(STATUS_OK_WITHOUT_RESULT):
        log_test_framework(LOG_TAG, 'ok without result')
    if response_line.startswith(STATUS_OK_WITH_RESULT):
        log_test_framework(LOG_TAG, 'ok with result')
        return response_line[len(STATUS_OK_WITH_RESULT + SPACE):]
    if response_line.startswith(STATUS_ASSERT_FAILED):
        current_case_continue_flag = False
        log_test_framework(LOG_TAG, response_line[len(STATUS_ASSERT_FAILED + SPACE):])
        raise AssertFailedException(response_line[len(STATUS_ASSERT_FAILED + SPACE):])

#send msg to server and get response
def interact_with_qsst_server(cmd):
    '''
    send request command line to server and get response
    line from server.The format of request and response should
    match with server side, so if you want to make any change please
    get familiar with the format of request and responses.

    @type cmd: string
    @param cmd: request command line.
    @todo: should not use contiue flag, use exceptions.
    '''
    if not can_continue():
        return

    global current_case_continue_flag
    log_test_framework(LOG_TAG, 'send: ' + cmd)
    send_result = my_socket_qsst.send_msg_line(cmd)
    if not send_result:
        current_case_continue_flag = False
        raise SocketException('send message failed')
    response = ['']
    recv_result = my_socket_qsst.get_response_line(response)
    if not recv_result:
        current_case_continue_flag = False
        raise SocketException('receive message failed')
    response_line = response[0]
    log_test_framework(LOG_TAG, 'receive: ' + response_line)
    if response_line.startswith(STATUS_OK_WITHOUT_RESULT):
        log_test_framework(LOG_TAG, 'ok without result')
    if response_line.startswith(STATUS_OK_WITH_RESULT):
        log_test_framework(LOG_TAG, 'ok with result')
        return response_line[len(STATUS_OK_WITH_RESULT + SPACE):]
    if response_line.startswith(STATUS_ASSERT_FAILED):
        current_case_continue_flag = False
        log_test_framework(LOG_TAG, response_line[len(STATUS_ASSERT_FAILED + SPACE):])
        raise AssertFailedException(response_line[len(STATUS_ASSERT_FAILED + SPACE):])

#given inputs, generate a cmd string
#note that all inputs are strings, except for value_list, it is a list
def generate_cmd(action, dest_view_type, dest_view_id_type, dest_view_id, value_list):
    '''
    generate a command line request for uiautomator server to perform an ui detection or operation. Lots of operations in L{case utility<case_utility>} used this api to generate requests, which can be your reference.

    @type action:int
    @param action: which action you want to perform.
    @type dest_view_type: int
    @param dest_view_type: the view's type you want to operate.
    @type dest_view_id_type: int
    @param dest_view_id_type: the id type you want to identify your view,which may be resource id,text,index,desc and so on, refer L{case_utility<case_utility>}
    @type value_list:list
    @param value_list: all other values, refer L{case_utility<case_utility>}.

    '''
    cmd_string = ACTION_TAG + action
    if len(dest_view_type) > 0:
        temp = SEPERATOR + DEST_VIEW_TYPE_TAG + dest_view_type
        cmd_string += temp
    if len(dest_view_id_type) > 0:
        temp = SEPERATOR + DEST_VIEW_ID_TYPE_TAG + dest_view_id_type
        cmd_string += temp
    if len(dest_view_id) > 0:
        temp = SEPERATOR + DEST_VIEW_ID_TAG + dest_view_id
        cmd_string += temp
    if len(value_list) > 0:
        for value in value_list:
            if len(value) > 0:
                temp = SEPERATOR + VALUE_TAG + value
                cmd_string += temp
    temp = LENGTH_TAG + str(len(cmd_string)) + SEPERATOR
    cmd_string = temp + cmd_string
    return cmd_string

def end_test_runners_accessibility():
    '''
    send command to uiautomator server to end
    the current test, it will close client socket at the same time.
    '''
    log_test_framework(LOG_TAG, "end test runner")
    cmd = generate_cmd(ACTION_END, '', '', '', [])
    interact_with_server(cmd)
    global my_socket
    my_socket.close()
    global my_socket_qsst
    my_socket_qsst.close()

def init_socket(local_socket_name, local_socket_name_for_qsst):
    '''
    setup a global socket for client.

    @type local_socket_name:string
    @param local_socket_name: socket name for uiautomator.
    @param local_socket_name_for_qsst: socket name for qsstservice.
    @return: True on success, False on fail.
    '''
    global my_socket
    global my_socket_qsst
    try:
        temp = SocketUtil(local_socket_name, 6100)
        temp_qsst = SocketUtil(local_socket_name_for_qsst, 6200)
        my_socket = temp
        my_socket_qsst = temp_qsst
    except IOError, msg:
        my_socket = None
        my_socket_qsst = None
        return False
    return True

def can_continue():
    '''
    return L{current_case_continue_flag<current_case_continue_flag>}

    @todo: should not use this, enhance to exceptions.
    '''
    global current_case_continue_flag
    return current_case_continue_flag

def set_cannot_continue():
    '''
    set L{current_case_continue_flag<current_case_continue_flag>} to False.
    This global flag used to judge if test can continue or not.

    @todo:should not use this ,enhance to exceptions.
    '''
    global current_case_continue_flag
    current_case_continue_flag = False

def set_can_continue():
    '''
    set L{current_case_continue_flag<current_case_continue_flag>} to True.

    @todo:should not use this, enhance to exceptions.
    '''
    global current_case_continue_flag
    current_case_continue_flag = True

def kill_by_name(pro_name):
    '''
    kill a process by given it's process name.

    @type pro_name: string
    @param pro_name: process name.
    @return: none
    '''
    os_info = get_platform_info()
    ps_cmd = None
    if os_info == "Linux-Phone":
        ps_cmd = ['ps']
    else:
        ps_cmd = ['adb', 'shell', 'ps']
    p = subprocess.Popen(ps_cmd,stdout=subprocess.PIPE)
    out = p.communicate()[0]
    for line in out.splitlines():
        if pro_name in line:
            pid = int(line.split()[1])
            if os_info == "Linux-Phone":
                os.kill(pid,signal.SIGKILL)
            else:
                subprocess.call(['adb', 'shell', 'kill', str(pid)])

def Host_Start_Uiautomator():
    print("before launch uiautomator")
    os.system('adb shell uiautomator translatecases &')

def init_acessibility_socket():
    '''
    Initialize server side socket, it will start up uiautomator socket.
    If used on PC , it will use also used adb forward  tcp:6100 to remote uiautomator
    socket running on device.
    '''
    kill_by_name('uiautomator')
    osInfo = get_platform_info()
    if(osInfo == "Windows" or osInfo == "Linux-PC"):
        os.system('adb shell am startservice -n com.android.qrdtest/.QsstService')
        os.system('adb forward tcp:6200 localabstract:myqsstservice')
        #subprocess.Popen(["adb", "shell", "uiautomator translatecases &"],stdout=subprocess.PIPE)
        thread.start_new_thread(Host_Start_Uiautomator, ())
        os.system('adb forward tcp:6100 localabstract:myuiautomator')
        #subprocess.Popen(cmd)
        pass
    elif(osInfo == "Linux-Phone"):
        os.system('am startservice -n com.android.qrdtest/.QsstService')
        os.system('uiautomator translatecases &')
    time.sleep(4)
    if not init_socket('\0' + fs_wrapper.ACCESSIBILITY_SOCKET_NAME, '\0' + fs_wrapper.QSSTSERVICE_SOCKET_NAME):
        print_report_line('init accessibility socket fail')
        return False
    return True

def wakeUpSignalHandler(a,b):
    '''
    wake up handler for sleep, not used currently.
    '''
    log_test_framework(LOG_TAG, "device wakes up");


def OnshakeSignal_handler(a, b):
    log_test_framework(LOG_TAG, "get device shake java to python signal,--- 1")


def getprop_suspend():
    os_info = get_platform_info()
    ps_cmd = None
    if os_info == "Linux-Phone":
        ps_cmd = ['getprop','python.process.suspend']
    else:
        ps_cmd = ['adb', 'shell', 'getprop','python.process.suspend']
    p = subprocess.Popen(ps_cmd,stdout=subprocess.PIPE)
    out = p.communicate()[0]
    for line in out.splitlines():
        if 'true' in line:
            log_test_framework(LOG_TAG, "suspend_flag = true, ---2 getprop");
            return True
    log_test_framework(LOG_TAG, "suspend_flag = false, ---2  getprop");
    return False

def kpi_path():
    '''
    This function used to save the log on the path. Weight and Data also on the path.
    @return: kpi_path
    '''
    osInfo = get_platform_info()
    kpi_path = sys.path[0] + os.sep + 'kpi'+os.sep
    return kpi_path

def kpi_log_value(category,casename,value):
    '''
    This function used to load-in data.
    @type category: string
    @param category: Category name,such as "launch-time","fps"
    @type casename: string
    @param casename:Test case name,such as "camera_001","browser"
    @type value: int
    @param value: such as 1000,200
    @return: kpi_log_value(category,casename,value)
    '''
    path = log_path()
    if not os.path.exists(path):
        os.makedirs(path)
    try:
        log = open(path + 'kpi_log.Qsst', 'ab')
    except Exception:
        print "utility.py kpi_log_value() log.txt lose"
    log.write("#" + category + ":" + casename + ":" + str(value)+ "\n")
    log.close()

def InvokeFuncByCurRunTarget(location,test_case,diff_api):
    '''
    This function used to get phone software version number.
    @type location: string
    @param location: platform file location.
    @type test_case:
    @param test_case:Test_case_name & adaptive.
    @type diff_api: string
    @param diff_api: replace api
    @return: replace api
    '''
    import settings.common as SC
    gtype = SC.PUBLIC_PHONE_PLATFORM_TYPE
    try:
        if gtype != '':
            module_meta = __import__(location+".platform."+gtype+"."+test_case, globals(), locals(),diff_api)
            fun_meta = getattr(module_meta, diff_api)
            fun_meta()
    except Exception as e:
            log_test_framework(test_case,"Error :" + str(gtype) +"can't find")
            
def isAliveforProcess(pro_name):
    '''
    check a process's living state by given it's process name.
    
    @type pro_name: string
    @param pro_name: process name.
    @return: boolean
    '''
    os_info = get_platform_info()
    ps_cmd = None
    if os_info == "Linux-Phone":
        ps_cmd = ['ps']
    else:
        ps_cmd = ['adb', 'shell', 'ps']
        p = subprocess.Popen(ps_cmd,stdout=subprocess.PIPE)
        out = p.communicate()[0]
    for line in out.splitlines():
        if pro_name in line:
            return True
    return False