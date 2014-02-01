'''
   case level utility for case writers

   This module will provide api to simulate user operation in DUT,get DUT info,
   status,context and so on.

   1.The api provided by this file is used for cases directly.

   2.If you want to add more similar to, you can add it here.
   Parts of api will communicate with uiautomator which play as a server. The api
   has a similar template.Before you add, recommend refer to existed api.


   @author: U{c_huangl<c_huangl@qti.qualcomm.com>}
   @version: version 1.0.0
   @requires:python 2.7+
   @license:

   @see: L{utility_wrapper <utility_wrapper>}
   @see: L{platform_check<platform_check>}
   @see: L{logging_wrapper<logging_wrapper>}
   @note:
   @attention:
   @bug:
   @warning:



'''
from utility_wrapper import *
from platform_check import get_platform_info
from logging_wrapper import *
import time
from subprocess import PIPE, Popen
import os
import signal

_LOG_TAG = 'case_utility'

'''action value used for communicating with uiautomator'''
#ACTION_END = '0'
ACTION_CLICK = '1'
ACTION_GO_BACK = '2'
ACTION_ENTER_TEXT = '3'
ACTION_SCREENSHOT = '4'
ACTION_RESTART_APP = '5'
ACTION_SHUTDOWN_APP ='6'
ACTION_START_APP = '7'
ACTION_DRAG = '8'
ACTION_SEND_KEY = '9'
ACTION_SEARCH_TEXT = '10'
#ACTION_START_ACTIVITY = '11'
ACTION_SEARCH_WEBVIEW_TITLE = '11'
ACTION_GET_BOOLEAN = '12'
ACTION_SET_VALUE = '13'
ACTION_SEARCH_VIEW = '14'
ACTION_CHECK_EXTERNAL_STORAGE = '15'
ACTION_CHECK_SYSTEM_LANGUAGE = '16'
ACTION_GET_ACTIVITY_NAME = '17'
ACTION_GET_VIEW_STATUS = '18'
ACTION_CLICK_BLIND = '19'
ACTION_LONG_CLICK = '20'
ACTION_CLEAR_TEXT = '21'
ACTION_UPDATE_REGISTER = '22'
ACTION_UPDATE_UNREGISTER = '23'
ACTION_DOUBLE_CLICK = '24'
ACTION_ZOOM = '25'
ACTION_GET_DISPLAY_WIDTH = '26'
ACTION_GET_DISPLAY_HEIGHT = '27'
ACTION_SLEEP = '28'
ACTION_WAKEUP = '29'
ACTION_ALARMER_UNREGISTER = '30'
ACTION_SEND_MMS = '31'
ACTION_ENABLE_SCROLL_PROFILING = '32'
ACTION_DISABLE_SCROLL_PROFILING = '33'
ACTION_GET_TEXT = '34'
ACTION_GET_POSTION = '35'
ACTION_GET_SPEED = '36'
ACTION_GET_BATTERY_TEMPERATE = '37'
ACTION_GET_ORIENTATION = '38'
ACTION_GET_AVAILABLE_RAM = '39'
ACTION_GET_AVAILABLE_ROM = '40'
ACTION_GET_WIFI_RSSI = '41'
ACTION_MT_TRIGGER_SERVICE = '43'
ACTION_UPDATE_NOTIFICATION = '44'
ACTION_GET_SIM_CARD_STATE = '45'
ACTION_GET_SIM_CARD_RSSI = '46'
ACTION_CHECK_BLUETOOTH = '47'
ACTION_CHECK_WIFI = '48'
ACTION_GET_VIEW_TEXT = '49'
ACTION_GET_VIEW_ENABLED = '50'
ACTION_GET_NETWORKTYPE = '51'
ACTION_WATCHER_REGISTER = '52'
ACTION_LEFT_DRAG = '53'
ACTION_RIGHT_DRAG = '54'

'''temperate unit'''
#temperate unit
#Celsius
TEMP_UNIT_C = '0'
#Fahrenheit
TEMP_UNIT_F = '1'

'''SIM card'''
#slot1
SLOT_ONE = '0'
#slot2
SLOT_TWO = '1'

'''SIM card state'''
#no SIM card is available in the device
SIM_STATE_ABSENT = 'no available sim card'
#Ready.
SIM_STATE_READY = 'ready'
#SIM Card Deactivated
SIM_STATE_DEACTIVATED = 'deactivated'
#SIM card is unknown or locked or error.
SIM_STATE_UNKNOWN = 'unknown or locked or error'

'''RSSI of SIM card '''
#none or unknown signal strength.
SIGNAL_STRENGTH_NONE_OR_UNKNOWN = 'none or unknown'
#poor signal strength.
SIGNAL_STRENGTH_POOR = 'poor'
#moderate signal strength.
SIGNAL_STRENGTH_MODERATE = 'moderate'
#good signal strength.
SIGNAL_STRENGTH_GOOD = 'good'
#great signal strength.
SIGNAL_STRENGTH_GREAT = 'great'

'''view used for action'''
VIEW_MENU_ITEM = '0'
VIEW_TEXT_VIEW = '1'
VIEW_EDIT_TEXT = '2'
VIEW_IMAGE_VIEW = '3'
VIEW_BUTTON = '4'
VIEW_CHECKBOX = '5'
VIEW_LIST = '6'
VIEW_TOGGLEBUTTON = '7'
VIEW_COMPOUNDBUTTON = '8'
VIEW_PROGRESSBAR = '9'

'''type id used for view'''
ID_TYPE_ID = '0'
ID_TYPE_TEXT = '1'
ID_TYPE_INDEX = '2'
ID_TYPE_FOCUSED = '3'
ID_TYPE_DESC = '4'

'''search type'''
#search flag
TEXT_MATCHES = '0'
TEXT_CONTAINS= '1'
TEXT_STARTS_WITH = '2'
TEXT_MATCHES_REGEX = '3'

'''types of scroll screen'''
#specific values
DRAG_UP = '1'
DRAG_DOWN = '2'
DRAG_TO_BOTTOM = '4'
DRAG_TO_TOP = '3'
DRAG_BY_PARAMETER = '0'
ZOOM_DOWN = '5'
ZOOM_UP = '6'

'''values of boolean'''
#for bool
BOOL_TRUE = 'true'
BOOL_FALSE = 'false'

'''keys for send action'''
#for action send key
KEY_RIGHT = '22'
KEY_LEFT = '21'
KEY_UP = '19'
KEY_DOWN = '20'
KEY_ENTER = '66'
KEY_MENU = '82'
KEY_DEL = '67'
KEY_HOME = '3'
KEYCODE_POWER = '26'

'''press type'''
#press type
SHORT_PRESS = '0'
LONG_PRESS = '1'

'''click type'''
#click type
SHORT_CLICK = '0'
LONG_CLICK = '1'

'''view status'''
#view status
VIEW_STATUS_CHECK = '1'
VIEW_STATUS_SELECT = '2'

'''wait time for pause python process'''
WAIT_TIME = 20

#if assert failes during one case or not
#can_continue() = True
#click text view
#isVerticaList: 1 for VerticalList, and 0 for HorizontalList
#isScrollable:  1 for Scrollable, and 0 for disable scroll
#waitForView: 1 for wait for new Window Change Event, and 0 for just click at once.
def click_textview_by_id(_id, isVerticalList=1, isScrollable=1, waitForView=0, clickType=SHORT_CLICK):
    '''
    click textview by id.

    @type _id: string
    @param _id: id of textview.
    @type isVerticalList: number
    @param isVerticalList: search direction,1:vertical; 0:horizontal.
    @type isScrollable: number
    @param isScrollable: whether scroll when search textview id,1:scrollable; 0:disable scroll.
    @type waitForView: number
    @param waitForView: whether wait for new window change event,1:wait for; 0:click at once.
    @type clickType: string
    @param clickType: click type,SHORT_CLICK:Short click; LONG_CLICK:long click.

    '''
    if not can_continue():
        return
    assert_type_string(_id)
    assert_type_int(isVerticalList)
    assert_type_int(isScrollable)
    assert_type_int(waitForView)
    assert_type_string(clickType)
    cmd = generate_cmd(ACTION_CLICK, VIEW_TEXT_VIEW, ID_TYPE_ID, _id, [str(isVerticalList), str(isScrollable), TEXT_STARTS_WITH , str(waitForView), clickType])
    interact_with_server(cmd)

#isVerticaList: 1 for VerticalList, and 0 for HorizontalList
#isScrollable:  1 for Scrollable, and 0 for disable scroll
def click_textview_by_text(text, isVerticalList=1, isScrollable=1, searchFlag=TEXT_STARTS_WITH, waitForView=0, clickType=SHORT_CLICK):
    '''
    click textview by text.

    @type text: string
    @param text: text of textview.
    @type isVerticalList: number
    @param isVerticalList: search direction,1:vertical; 0:horizontal.
    @type isScrollable: number
    @param isScrollable: whether scroll when search textview id,1:scrollable; 0:disable scroll.
    @type searchFlag: string
    @param searchFlag: matching type, TEXT_MATCHES:text perfect matching; TEXT_CONTAINS:text partial matching;
                       TEXT_STARTS_WITH: matching string the text string starts with; TEXT_MATCHES_REGEX: matching with regex.
    @type waitForView: number
    @param waitForView: whether wait for new window change event,1:wait for; 0:click at once.
    @type clickType: string
    @param clickType: click type,SHORT_CLICK:Short click; LONG_CLICK:long click.

    '''
    if not can_continue():
        return
    assert_type_string(text)
    assert_type_int(isVerticalList)
    assert_type_int(isScrollable)
    assert_type_string(searchFlag)
    assert_type_int(waitForView)
    assert_type_string(clickType)
    cmd = generate_cmd(ACTION_CLICK, VIEW_TEXT_VIEW, ID_TYPE_TEXT, text, [str(isVerticalList), str(isScrollable), searchFlag, str(waitForView), clickType])
    interact_with_server(cmd)

#isVerticaList: 1 for VerticalList, and 0 for HorizontalList
#isScrollable:  1 for Scrollable, and 0 for disable scroll
def click_textview_by_desc(desc, isVerticalList=1, isScrollable=1, waitForView=0, clickType=SHORT_CLICK):
    '''
    click textview by desc.

    @type desc: string
    @param desc: description of textview.
    @type isVerticalList: number
    @param isVerticalList: search direction,1:vertical; 0:horizontal.
    @type isScrollable: number
    @param isScrollable: whether scroll when search textview id,1:scrollable; 0:disable scroll.
    @type waitForView: number
    @param waitForView: whether wait for new window change event,1:wait for; 0:click at once.
    @type clickType: string
    @param clickType: click type,SHORT_CLICK:Short click; LONG_CLICK:long click.

    '''
    if not can_continue():
        return
    assert_type_string(desc)
    assert_type_int(isVerticalList)
    assert_type_int(isScrollable)
    assert_type_int(waitForView)
    assert_type_string(clickType)
    cmd = generate_cmd(ACTION_CLICK, VIEW_TEXT_VIEW, ID_TYPE_DESC, desc, [str(isVerticalList), str(isScrollable), TEXT_STARTS_WITH, str(waitForView), clickType])
    interact_with_server(cmd)

def get_textview_select_by_text(text):
    '''
    check whether exists the textview by the text.

    @type text: string
    @param text: text of textview.
    @return: True:exist, False:not exist.
    '''
    if not can_continue():
        return
    assert_type_string(text)
    cmd = generate_cmd(ACTION_GET_VIEW_STATUS, VIEW_TEXT_VIEW, ID_TYPE_DESC, text, [VIEW_STATUS_SELECT])
    result = interact_with_server(cmd)
    if result == BOOL_TRUE:
        return True
    elif result == BOOL_FALSE:
        return False

def get_view_text_by_id(view_type, _id, isVerticalList=1, isScrollable=1):
    '''
    get view'text by id
    The view can be textview,edittext,button,checkbox.

    @type view_type: string
    @param view_type: the type of view. can be VIEW_TEXT_VIEW,VIEW_EDIT_TEXT,VIEW_BUTTON,VIEW_CHECKBOX.
    @type _id: string
    @param _id: id of textview.
    @type isVerticalList: number
    @param isVerticalList: search direction,1:vertical; 0:horizontal.
    @type isScrollable: number
    @param isScrollable: whether scroll when search textview id,1:scrollable; 0:disable scroll.
    @return: the text of view
    '''
    if not can_continue():
        return
    assert_type_string(view_type)
    assert_type_string(_id)
    assert_type_int(isVerticalList)
    assert_type_int(isScrollable)
    cmd = __generate_cmd_for_view_text(view_type, ID_TYPE_ID, _id, isVerticalList, isScrollable)
    result = interact_with_server(cmd)
    return result

def get_view_text_by_index(view_type, index):
    '''
    get view'text by index
    The view can be textview,edittext,button,checkbox.

    @type view_type: string
    @param view_type: the type of view. can be VIEW_TEXT_VIEW,VIEW_EDIT_TEXT,VIEW_BUTTON,VIEW_CHECKBOX.
    @type index: number
    @param index: index of textview.
    @return: the text of view
    '''
    if not can_continue():
        return
    assert_type_string(view_type)
    assert_type_int(index)
    cmd = __generate_cmd_for_view_text(view_type, ID_TYPE_INDEX, index)
    result = interact_with_server(cmd)
    return result

def click_textview_by_index(index):
    '''
    click textview by index.

    @type index: number
    @param index: index of textview.

    '''
    if not can_continue():
        return
    assert_type_int(index)
    cmd = generate_cmd(ACTION_CLICK, VIEW_TEXT_VIEW, ID_TYPE_INDEX, str(index), [])
    interact_with_server(cmd)

def click_in_list_by_index(index):
    '''
    click list by index.

    @type index: number
    @param index: index of list.

    '''
    if not can_continue():
        return
    assert_type_int(index)
    #all index should start from 0
    cmd = generate_cmd(ACTION_CLICK, VIEW_LIST, ID_TYPE_INDEX, str(index + 1), [])
    interact_with_server(cmd)

#click menu item
#isVerticaList: 1 for VerticalList, and 0 for HorizontalList
#isScrollable:  1 for Scrollable, and 0 for disable scroll
def click_menuitem_by_text(text, isVerticalList=1, isScrollable=1, searchFlag=TEXT_STARTS_WITH, waitForView=0, clickType=SHORT_CLICK):
    '''
    click menuitem by text.

    @type text: string
    @param text: text of textview.
    @type isVerticalList: number
    @param isVerticalList: search direction,1:vertical; 0:horizontal.
    @type isScrollable: number
    @param isScrollable: whether scroll when search textview id,1:scrollable; 0:disable scroll.
    @type searchFlag: string
    @param searchFlag: matching type, TEXT_MATCHES:text perfect matching; TEXT_CONTAINS:text partial matching;
                       TEXT_STARTS_WITH: matching string the text string starts with; TEXT_MATCHES_REGEX: matching with regex.
    @type waitForView: number
    @param waitForView: whether wait for new window change event,1:wait for; 0:click at once.
    @type clickType: string
    @param clickType: click type,SHORT_CLICK:Short click; LONG_CLICK:long click.

    '''
    if not can_continue():
        return
    assert_type_string(text)
    assert_type_int(isVerticalList)
    assert_type_int(isScrollable)
    assert_type_string(searchFlag)
    assert_type_int(waitForView)
    assert_type_string(clickType)
    cmd = generate_cmd(ACTION_CLICK, VIEW_MENU_ITEM, ID_TYPE_TEXT, text, [str(isVerticalList), str(isScrollable), searchFlag, str(waitForView), clickType])
    interact_with_server(cmd)

#click image view
def click_imageview_by_index(index):
    '''
    click imageview by index.

    @type index: number
    @param index: index of imageview.

    '''
    if not can_continue():
        return
    assert_type_int(index)
    cmd = generate_cmd(ACTION_CLICK, VIEW_IMAGE_VIEW, ID_TYPE_INDEX, str(index), [])
    interact_with_server(cmd)

#isVerticaList: 1 for VerticalList, and 0 for HorizontalList
#isScrollable:  1 for Scrollable, and 0 for disable scroll
def click_imageview_by_id(_id, isVerticalList=1, isScrollable=1, waitForView=0, clickType=SHORT_CLICK):
    '''
    click imageview by id.

    @type _id: number
    @param _id: id of textview.
    @type isVerticalList: number
    @param isVerticalList: search direction,1:vertical; 0:horizontal.
    @type isScrollable: number
    @param isScrollable: whether scroll when search textview id,1:scrollable; 0:disable scroll.
    @type waitForView: number
    @param waitForView: whether wait for new window change event,1:wait for; 0:click at once.
    @type clickType: string
    @param clickType: click type,SHORT_CLICK:Short click; LONG_CLICK:long click.

    '''
    if not can_continue():
        return
    assert_type_string(_id)
    assert_type_int(isVerticalList)
    assert_type_int(isScrollable)
    assert_type_int(waitForView)
    assert_type_string(clickType)
    cmd = generate_cmd(ACTION_CLICK, VIEW_IMAGE_VIEW, ID_TYPE_ID, _id, [str(isVerticalList), str(isScrollable), TEXT_STARTS_WITH, str(waitForView), clickType])
    interact_with_server(cmd)

#isVerticaList: 1 for VerticalList, and 0 for HorizontalList
#isScrollable:  1 for Scrollable, and 0 for disable scroll
def click_imageview_by_desc(desc, isVerticalList=1, isScrollable=1, waitForView=0, clickType=SHORT_CLICK):
    '''
    click imageview by description.

    @type desc: description
    @param desc: description of textview.
    @type isVerticalList: number
    @param isVerticalList: search direction,1:vertical; 0:horizontal.
    @type isScrollable: number
    @param isScrollable: whether scroll when search textview id,1:scrollable; 0:disable scroll.
    @type waitForView: number
    @param waitForView: whether wait for new window change event,1:wait for; 0:click at once.
    @type clickType: string
    @param clickType: click type,SHORT_CLICK:Short click; LONG_CLICK:long click.

    '''
    if not can_continue():
        return
    assert_type_string(desc)
    assert_type_int(isVerticalList)
    assert_type_int(isScrollable)
    assert_type_int(waitForView)
    assert_type_string(clickType)
    cmd = generate_cmd(ACTION_CLICK, VIEW_IMAGE_VIEW, ID_TYPE_DESC, desc,[str(isVerticalList), str(isScrollable), TEXT_STARTS_WITH, str(waitForView), clickType])
    interact_with_server(cmd)

#click button
def click_button_by_index(index):
    '''
    click button by index.

    @type index: number
    @param index: index of button.

    '''
    if not can_continue():
        return
    assert_type_int(index)
    cmd = generate_cmd(ACTION_CLICK, VIEW_BUTTON, ID_TYPE_INDEX, str(index), [])
    interact_with_server(cmd)

#isVerticaList: 1 for VerticalList, and 0 for HorizontalList
#isScrollable:  1 for Scrollable, and 0 for disable scroll
def click_button_by_id(_id, isVerticalList=1, isScrollable=1, waitForView=0, clickType=SHORT_CLICK):
    '''
    click button by id.

    @type _id: id
    @param _id: id of button.
    @type isVerticalList: number
    @param isVerticalList: search direction,1:vertical; 0:horizontal.
    @type isScrollable: number
    @param isScrollable: whether scroll when search textview id,1:scrollable; 0:disable scroll.
    @type waitForView: number
    @param waitForView: whether wait for new window change event,1:wait for; 0:click at once.
    @type clickType: string
    @param clickType: click type,SHORT_CLICK:Short click; LONG_CLICK:long click.

    '''
    if not can_continue():
        return
    assert_type_string(_id)
    assert_type_int(isVerticalList)
    assert_type_int(isScrollable)
    assert_type_int(waitForView)
    assert_type_string(clickType)
    cmd = generate_cmd(ACTION_CLICK, VIEW_BUTTON, ID_TYPE_ID, _id, [str(isVerticalList), str(isScrollable), TEXT_STARTS_WITH, str(waitForView), clickType])
    interact_with_server(cmd)

#isVerticaList: 1 for VerticalList, and 0 for HorizontalList
#isScrollable:  1 for Scrollable, and 0 for disable scroll
def click_button_by_text(text, isVerticalList=1, isScrollable=1, searchFlag=TEXT_STARTS_WITH, waitForView=0, clickType=SHORT_CLICK):
    '''
    click button by text.

    @type text: String
    @param text: text of button.
    @type isVerticalList: number
    @param isVerticalList: search direction,1:vertical; 0:horizontal.
    @type isScrollable: number
    @param isScrollable: whether scroll when search textview id,1:scrollable; 0:disable scroll.
    @type searchFlag: string
    @param searchFlag: matching type, TEXT_MATCHES:text perfect matching; TEXT_CONTAINS:text partial matching;
                       TEXT_STARTS_WITH: matching string the text string starts with; TEXT_MATCHES_REGEX: matching with regex.
    @type waitForView: number
    @param waitForView: whether wait for new window change event,1:wait for; 0:click at once.
    @type clickType: string
    @param clickType: click type,SHORT_CLICK:Short click; LONG_CLICK:long click.

    '''
    if not can_continue():
        return
    assert_type_string(text)
    assert_type_int(isVerticalList)
    assert_type_int(isScrollable)
    assert_type_string(searchFlag)
    assert_type_int(waitForView)
    assert_type_string(clickType)
    cmd = generate_cmd(ACTION_CLICK, VIEW_BUTTON, ID_TYPE_TEXT, text, [str(isVerticalList), str(isScrollable), searchFlag, str(waitForView), clickType])
    interact_with_server(cmd)

def click_checkbox_by_index(index):
    '''
    click checkbox by index.

    @type index: number
    @param index: index of checkbox.

    '''
    if not can_continue():
        return
    assert_type_int(index)
    cmd = generate_cmd(ACTION_CLICK, VIEW_CHECKBOX, ID_TYPE_INDEX, str(index), [])
    interact_with_server(cmd)

#isVerticaList: 1 for VerticalList, and 0 for HorizontalList
#isScrollable:  1 for Scrollable, and 0 for disable scroll
def click_checkbox_by_id(_id, isVerticalList=1, isScrollable=1, waitForView=0, clickType=SHORT_CLICK):
    '''
    click checkbox by id.

    @type _id: id
    @param _id: id of checkbox.
    @type isVerticalList: number
    @param isVerticalList: search direction,1:vertical; 0:horizontal.
    @type isScrollable: number
    @param isScrollable: whether scroll when search textview id,1:scrollable; 0:disable scroll.
    @type waitForView: number
    @param waitForView: whether wait for new window change event,1:wait for; 0:click at once.
    @type clickType: string
    @param clickType: click type,SHORT_CLICK:Short click; LONG_CLICK:long click.

    '''
    if not can_continue():
        return
    assert_type_string(_id)
    assert_type_int(isVerticalList)
    assert_type_int(isScrollable)
    assert_type_int(waitForView)
    assert_type_string(clickType)
    cmd = generate_cmd(ACTION_CLICK, VIEW_CHECKBOX, ID_TYPE_ID, _id, [str(isVerticalList), str(isScrollable), TEXT_STARTS_WITH, str(waitForView), clickType])
    interact_with_server(cmd)

#className should be the UI item's class name.
def click_view_by_container_id(_id, className, index):
    '''
    click view by layout id ,the index of the view in layout and UI item's class name when can not directly click the view by its attribute.

    @type _id: id
    @param _id: id of layout.
    @type className: String
    @param className: should be the UI item's class name.
    @type index: number
    @param index: the index of the view in layout.

    '''
    if not can_continue():
        return
    assert_type_string(_id)
    assert_type_string(className)
    assert_type_int(index)
    cmd = generate_cmd(ACTION_CLICK_BLIND, '', ID_TYPE_ID, _id, [className, str(index)])
    interact_with_server(cmd)

#className should be the UI item's class name.
def click_view_by_container_desc(desc, className, index):
    '''
    click view by layout description ,the index of the view in layout and UI item's class name when the view has no description.

    @type desc: description
    @param desc: description of layout.
    @type className: String
    @param className: should be the UI item's class name.
    @type index: number
    @param index: the index of the view in layout.

    '''
    if not can_continue():
        return
    assert_type_string(desc)
    assert_type_string(className)
    assert_type_int(index)
    cmd = generate_cmd(ACTION_CLICK_BLIND, '', ID_TYPE_DESC, desc, [className, str(index)])
    interact_with_server(cmd)

def long_click(x, y):
    '''
    long click screen by coordinate point.

    @type x: number
    @param x: x-coordinate point.
    @type y: number
    @param y: y-coordinate point.

    '''
    if not can_continue():
        return
    assert_type_int(x)
    assert_type_int(y)
    cmd = generate_cmd(ACTION_LONG_CLICK, '', '', '', [str(x), str(y)])
    interact_with_server(cmd)

def double_click(x, y):
    '''
    double click screen by coordinate point.

    @type x: number
    @param x: x-coordinate point.
    @type y: number
    @param y: y-coordinate point.

    '''
    if not can_continue():
        return
    assert_type_int(x)
    assert_type_int(y)
    cmd = generate_cmd(ACTION_DOUBLE_CLICK, '', '', '', [str(x), str(y)])
    interact_with_server(cmd)

#send key event
def send_key(key, keyType = SHORT_PRESS):
    '''
    send key event.

    @type key: String
    @param key: the defined key event value. Use the KEY_* variables
    @type keyType: String
    @param keyType: press type,SHORT_PRESS:short press; LONG_PRESS:long press.

    '''
    if not can_continue():
        return
    assert_type_string(key)
    cmd = generate_cmd(ACTION_SEND_KEY, '', '', '', [key, keyType])
    interact_with_server(cmd)

#drag event
def drag_by_param(startX, startY, endX, endY, stepCount):
    '''
    drag screen from one point to another point by some speed.

    @type startX: Number
    @param startX: start x-coordinate postion by percent
    @type startY: Number
    @param startY: start y-coordinate postion by percent
    @type endX: Number
    @param endX: end x-coordinate postion by percent
    @type endY: Number
    @param endY: end y-coordinate postion by percent
    @type stepCount: Number
    @param stepCount: the speed of drag. higher value, lower speed.

    '''
    if not can_continue():
        return
    assert_type_int(startX)  
    assert_type_int(startY)
    assert_type_int(endX)
    assert_type_int(endY)
    assert_type_int(stepCount)
    cmd = generate_cmd(ACTION_DRAG, '', '', '', [DRAG_BY_PARAMETER, str(startX), str(startY), str(endX), str(endY), str(stepCount)])
    interact_with_server(cmd)

def scroll_up():
    '''
    scroll up screen
    '''
    if not can_continue():
        return
    cmd = generate_cmd(ACTION_DRAG, '', '', '', [DRAG_UP])
    interact_with_server(cmd)

def scroll_down():
    '''
    scroll down screen
    '''
    if not can_continue():
        return
    cmd = generate_cmd(ACTION_DRAG, '', '', '', [DRAG_DOWN])
    interact_with_server(cmd)

def scroll_to_bottom():
    '''
    scroll screen to bottom
    '''
    if not can_continue():
        return
    cmd = generate_cmd(ACTION_DRAG, '', '', '', [DRAG_TO_BOTTOM])
    interact_with_server(cmd)

def scroll_to_top():
    '''
    scroll screen to top
    '''

    if not can_continue():
        return
    cmd = generate_cmd(ACTION_DRAG, '', '', '', [DRAG_TO_TOP])
    interact_with_server(cmd)

#enter edittext
def entertext_edittext_by_id(_id, value, isVerticalList=1, isScrollable=1, isClear=1):
    '''
    Input the text in edittext by id. When need clear firstly, set isClear as 1, otherwise 0.

    @type _id: string
    @param _id: id of edittext.
    @type value: string
    @param value: the enter value.
    @type isVerticalList: number
    @param isVerticalList: search direction,1:vertical; 0:horizontal.
    @type isScrollable: number
    @param isScrollable: whether scroll when search textview id,1:scrollable; 0:disable scroll.
    @type isClear: number
    @param isClear: whether clear old value firstly,1:need clear; 0:without clear.

    '''
    if not can_continue():
        return
    assert_type_string(_id)
    assert_type_int(isVerticalList)
    assert_type_int(isScrollable)
    assert_type_string(value)
    cmd = generate_cmd(ACTION_ENTER_TEXT, VIEW_EDIT_TEXT, ID_TYPE_ID, _id, [str(isVerticalList), str(isScrollable), value, str(isClear)])
    interact_with_server(cmd)

def entertext_edittext_by_index(index, value, isVerticalList=1, isScrollable=1, isClear=1):
    '''
    Input the text in edittext by index. When need clear firstly, set isClear as 1, otherwise 0.

    @type index: number
    @param index: index of edittext.
    @type value: string
    @param value: the enter value.
    @type isVerticalList: number
    @param isVerticalList: search direction,1:vertical; 0:horizontal.
    @type isScrollable: number
    @param isScrollable: whether scroll when search textview id,1:scrollable; 0:disable scroll.
    @type isClear: number
    @param isClear: whether clear old value firstly,1:need clear; 0:without clear.

    '''
    if not can_continue():
        return
    assert_type_int(index)
    assert_type_int(isVerticalList)
    assert_type_int(isScrollable)
    assert_type_string(value)
    cmd = generate_cmd(ACTION_ENTER_TEXT, VIEW_EDIT_TEXT, ID_TYPE_INDEX, str(index), [str(isVerticalList), str(isScrollable), value, str(isClear)])
    interact_with_server(cmd)

def entertext_edittext_on_focused(value, isVerticalList=1, isScrollable=1, isClear=1):
    '''
    Input the text in edittext by edittext value. When need clear firstly, set isClear as 1, otherwise 0.

    @type value: string
    @param value: the editext value.
    @type isVerticalList: number
    @param isVerticalList: search direction,1:vertical; 0:horizontal.
    @type isScrollable: number
    @param isScrollable: whether scroll when search textview id,1:scrollable; 0:disable scroll.
    @type isClear: number
    @param isClear: whether clear old value firstly,1:need clear; 0:without clear.

    '''
    if not can_continue():
        return
    assert_type_int(isVerticalList)
    assert_type_int(isScrollable)
    assert_type_string(value)
    cmd = generate_cmd(ACTION_ENTER_TEXT, VIEW_EDIT_TEXT, ID_TYPE_FOCUSED, '', [str(isVerticalList), str(isScrollable), value, str(isClear)])
    interact_with_server(cmd)

#clear edittext
def clear_edittext_by_id(_id, isVerticalList=1, isScrollable=1):
    '''
    clear edittext value by id.

    @type _id: string
    @param _id: id of editext.
    @type isVerticalList: number
    @param isVerticalList: search direction,1:vertical; 0:horizontal.
    @type isScrollable: number
    @param isScrollable: whether scroll when search textview id,1:scrollable; 0:disable scroll.

    '''
    if not can_continue():
        return
    assert_type_string(_id)
    assert_type_int(isVerticalList)
    assert_type_int(isScrollable)
    cmd = generate_cmd(ACTION_CLEAR_TEXT, VIEW_EDIT_TEXT, ID_TYPE_ID, _id, [str(isVerticalList), str(isScrollable)])
    interact_with_server(cmd)

def clear_edittext_by_index(index, isVerticalList=1, isScrollable=1):
    '''
    clear edittext value by index.

    @type index: number
    @param index: index of editext.
    @type isVerticalList: number
    @param isVerticalList: search direction,1:vertical; 0:horizontal.
    @type isScrollable: number
    @param isScrollable: whether scroll when search textview id,1:scrollable; 0:disable scroll.

    '''
    if not can_continue():
        return
    assert_type_int(index)
    assert_type_int(isVerticalList)
    assert_type_int(isScrollable)
    cmd = generate_cmd(ACTION_CLEAR_TEXT, VIEW_EDIT_TEXT, ID_TYPE_INDEX, str(index), [str(isVerticalList), str(isScrollable)])
    interact_with_server(cmd)

def clear_edittext_on_focused(isVerticalList=1, isScrollable=1):
    '''
    clear the focused edittext.

    @type isVerticalList: number
    @param isVerticalList: search direction,1:vertical; 0:horizontal.
    @type isScrollable: number
    @param isScrollable: whether scroll when search textview id,1:scrollable; 0:disable scroll.

    '''
    if not can_continue():
        return
    assert_type_int(isVerticalList)
    assert_type_int(isScrollable)
    cmd = generate_cmd(ACTION_CLEAR_TEXT, VIEW_EDIT_TEXT, ID_TYPE_FOCUSED, '', [str(isVerticalList), str(isScrollable)])
    interact_with_server(cmd)

#go back
#className: UI element name. eg: VIEW_PROGRESSBAR, VIEW_CHECKBOX and etc.
#idType: the category which id belongs to. eg: ID_TYPE_ID,ID_TYPE_TEXTS and etc.
def goback(className='', idType='', id=''):
    '''
    go back, that is click the back key.

    @type className: string
    @param className: no use.
    @type idType: string
    @param idType: no use.
    @type id: string
    @param id: no use.

    '''
    if not can_continue():
        return
    assert_type_string(className)
    assert_type_string(idType)
    assert_type_string(id)
    cmd = generate_cmd(ACTION_GO_BACK, className, idType, id, [])
    interact_with_server(cmd)

def shutdown():
    '''
    shut down current app
    '''
    if not can_continue():
        return
    cmd = generate_cmd(ACTION_SHUTDOWN_APP, '', '', '', [])
    interact_with_server(cmd)

def sleep(_time):
    '''
    sleep some time

    @type _time:number
    @param _time: the seconds of sleep time

    '''
    if not can_continue():
        return
    time.sleep(_time)

#search text
def search_text(text, isVerticalList=1, isScrollable=1, searchFlag=TEXT_STARTS_WITH):
    '''
    search text.

    @type text: string
    @param text: text of textview.
    @type isVerticalList: number
    @param isVerticalList: search direction,1:vertical; 0:horizontal.
    @type isScrollable: number
    @param isScrollable: whether scroll when search textview id,1:scrollable; 0:disable scroll.
    @type searchFlag: string
    @param searchFlag: matching type, TEXT_MATCHES:text perfect matching; TEXT_CONTAINS:text partial matching;
                       TEXT_STARTS_WITH: matching string the text string starts with; TEXT_MATCHES_REGEX: matching with regex.

    '''
    if not can_continue():
        return False
    assert_type_string(text)
    assert_type_int(isVerticalList)
    assert_type_int(isScrollable)
    assert_type_string(searchFlag)
    cmd = generate_cmd(ACTION_SEARCH_TEXT,'', '', '', [str(isVerticalList), str(isScrollable), text, searchFlag])
    result = interact_with_server(cmd)
    if result == BOOL_TRUE:
        return True
    elif result == BOOL_FALSE:
        return False

#get textView's text
def get_text(text, isVerticaList=0, isScrollable=0, searchFlag=TEXT_CONTAINS):
    '''
    get textView's text.

    @type text: string
    @param text: text of textview.
    @type isVerticaList: number
    @param isVerticaList: search direction,1:vertical; 0:horizontal.
    @type isScrollable: number
    @param isScrollable: whether scroll when search textview id,1:scrollable; 0:disable scroll.
    @type searchFlag: string
    @param searchFlag: matching type, TEXT_MATCHES:text perfect matching; TEXT_CONTAINS:text partial matching;
                       TEXT_STARTS_WITH: matching string the text string starts with; TEXT_MATCHES_REGEX: matching with regex.

    '''
    if not can_continue():
        return
    assert_type_string(text)
    assert_type_int(isVerticaList)
    assert_type_int(isScrollable)
    assert_type_string(searchFlag)
    cmd = generate_cmd(ACTION_GET_TEXT, '', '', '',[str(isVerticaList), str(isScrollable), text, searchFlag])
    result = interact_with_server(cmd)
    return result
#search webview title
def search_webview_title(title):
    '''
    search webview title.

    @type title: string
    @param title: title of webview.

    '''
    if not can_continue():
        return False
    assert_type_string(title)
    cmd = generate_cmd(ACTION_SEARCH_WEBVIEW_TITLE,'', '', '', [title])
    result = interact_with_server(cmd)
    if result == BOOL_TRUE:
        return True
    elif result == BOOL_FALSE:
        return False

#local function
def local_rm_dir(_dir):
    '''
    remove directory.

    @type _dir: string
    @param _dir: the directory.

    '''
    assert_type_string(_dir)
    os.system('rm -r ' + _dir)

def local_assert(expected, real):
    '''
    set whether continue in case. When expected value is not equal to real value ,then can not continue.

    @type expected: boolean
    @param expected: expected value.
    @type real: boolean
    @param real: real value.

    '''
    if not can_continue():
        return 
    if expected != real:
        set_cannot_continue()
        log_test_framework(_LOG_TAG, 'assert fail, real: ' + str(real) + ', expected: ' + str(expected))


def start_activity(package_name, activity_name):
    '''
    manual start activity.

    @type package_name: string
    @param package_name: package name of activity.
    @type activity_name: string
    @param activity_name: activity name.

    '''
    if not can_continue():
        return False
    assert_type_string(package_name)
    assert_type_string(activity_name)
    osInfo = get_platform_info()
    if(osInfo == 'Linux-Phone'):
        os.system("am start " + package_name + "/" + activity_name)
    elif(osInfo == 'Linux-PC' or osInfo =='Windows'):
        os.system("adb shell am start " + package_name + "/" + activity_name)

def reboot_phone():
    '''
    reboot phone.

    '''
    if not can_continue():
        return False
    osInfo = get_platform_info()
    if(osInfo == 'Linux-Phone'):
        os.system("reboot ")
    elif(osInfo == 'Linux-PC' or osInfo == 'Windows'):
        os.system("adb reboot ")

def is_cdma():
    '''
    check whether the network is CMDA or not.

    @return: True: CMDA; False: no.

    '''
    out=os.popen('getprop gsm.operator.numeric').read()
    if out == str("46003\n"):
        return True
    else:
        return False

def is_checkbox_checked_by_text(text):
    '''
    check checkbox whether is checked or not by text.

    @type text: string
    @param text: the text of checkbox

    '''
    if not can_continue():
        return
    assert_type_string(text)
    cmd = generate_cmd(ACTION_GET_BOOLEAN, VIEW_CHECKBOX, ID_TYPE_ID, text, [])
    result = interact_with_server(cmd)
    if result == BOOL_TRUE:
        return True
    elif result == BOOL_FALSE:
        return False

def is_checkbox_checked_by_index(index):
    '''
    check checkbox whether is checked or not by index.

    @type index: number
    @param index: the index of checkbox

    '''
    if not can_continue():
        return
    assert_type_int(index)
    cmd = generate_cmd(ACTION_GET_BOOLEAN, VIEW_CHECKBOX, ID_TYPE_INDEX, str(index), [])
    result = interact_with_server(cmd)
    if result == BOOL_TRUE:
        return True
    elif result == BOOL_FALSE:
        return False

def is_togglebutton_checked_by_text(text):
    '''
    check togglebutton whether is checked or not by text.

    @type text: string
    @param text: the text of togglebutton

    '''
    if not can_continue():
        return
    assert_type_string(text)
    cmd = generate_cmd(ACTION_GET_BOOLEAN, VIEW_TOGGLEBUTTON, ID_TYPE_ID, text, [])
    result = interact_with_server(cmd)
    if result == BOOL_TRUE:
        return True
    elif result == BOOL_FALSE:
        return False

def is_togglebutton_checked_by_index(index):
    '''
    check togglebutton whether is checked or not by index.

    @type index: number
    @param index: the index of togglebutton

    '''
    if not can_continue():
        return
    assert_type_int(index)
    cmd = generate_cmd(ACTION_GET_BOOLEAN, VIEW_TOGGLEBUTTON, ID_TYPE_INDEX, str(index), [])
    result = interact_with_server(cmd)
    if result == BOOL_TRUE:
        return True
    elif result == BOOL_FALSE:
        return False

def is_compoundbutton_checked_by_index(index):
    '''
    check compoundbutton whether is checked or not by index.

    @type index: number
    @param index: the index of compoundbutton

    '''
    if not can_continue():
        return
    assert_type_int(index)
    cmd = generate_cmd(ACTION_GET_BOOLEAN, VIEW_COMPOUNDBUTTON, ID_TYPE_INDEX, str(index), [])
    result = interact_with_server(cmd)
    if result == BOOL_TRUE:
        return True
    elif result == BOOL_FALSE:
        return False

def is_view_enabled_by_id(view_type, _id, isVerticalList=1, isScrollable=1):
    '''
    check view whether is enabled or not by id.
    The view can be textview,edittext,button,checkbox,imageview,togglebutton,compoundbutton.

    @type view_type: string
    @param view_type: the type of view. can be VIEW_TEXT_VIEW,VIEW_EDIT_TEXT,VIEW_BUTTON,VIEW_CHECKBOX,VIEW_IMAGE_VIEW,VIEW_TOGGLEBUTTON,VIEW_COMPOUNDBUTTON.
    @type id: number
    @param id: the id of textview
    @type isVerticalList: number
    @param isVerticalList: search direction,1:vertical; 0:horizontal.
    @type isScrollable: number
    @param isScrollable: whether scroll when search textview id,1:scrollable; 0:disable scroll.
    '''
    if not can_continue():
        return
    assert_type_string(view_type)
    assert_type_string(_id)
    assert_type_int(isVerticalList)
    assert_type_int(isScrollable)
    cmd = __generate_cmd_for_view_enabled(view_type, ID_TYPE_ID, _id, isVerticalList, isScrollable, TEXT_STARTS_WITH)
    result = interact_with_server(cmd)
    if result == BOOL_TRUE:
        return True
    elif result == BOOL_FALSE:
        return False

def is_view_enabled_by_text(view_type, text, isVerticalList=1, isScrollable=1, searchFlag=TEXT_STARTS_WITH):
    '''
    check view whether is enabled or not by text.
    The view can be textview,edittext,button,checkbox,imageview,togglebutton,compoundbutton.

    @type view_type: string
    @param view_type: the type of view. can be VIEW_TEXT_VIEW,VIEW_EDIT_TEXT,VIEW_BUTTON,VIEW_CHECKBOX,VIEW_IMAGE_VIEW,VIEW_TOGGLEBUTTON,VIEW_COMPOUNDBUTTON.
    @type text: string
    @param text: the text of textview
    @type isVerticalList: number
    @param isVerticalList: search direction,1:vertical; 0:horizontal.
    @type isScrollable: number
    @param isScrollable: whether scroll when search textview id,1:scrollable; 0:disable scroll.
    @type searchFlag: string
    @param searchFlag: matching type, TEXT_MATCHES:text perfect matching; TEXT_CONTAINS:text partial matching;
                       TEXT_STARTS_WITH: matching string the text string starts with; TEXT_MATCHES_REGEX: matching with regex.
    '''
    if not can_continue():
        return
    assert_type_string(view_type)
    assert_type_string(text)
    assert_type_int(isVerticalList)
    assert_type_int(isScrollable)
    assert_type_string(searchFlag)
    cmd = __generate_cmd_for_view_enabled(view_type, ID_TYPE_TEXT, text, isVerticalList, isScrollable, searchFlag)
    result = interact_with_server(cmd)
    if result == BOOL_TRUE:
        return True
    elif result == BOOL_FALSE:
        return False

def is_view_enabled_by_index(view_type, index):
    '''
    check view whether is enabled or not by index.
    The view can be textview,edittext,button,checkbox,imageview,togglebutton,compoundbutton.

    @type view_type: string
    @param view_type: the type of view. can be VIEW_TEXT_VIEW,VIEW_EDIT_TEXT,VIEW_BUTTON,VIEW_CHECKBOX,VIEW_IMAGE_VIEW,VIEW_TOGGLEBUTTON,VIEW_COMPOUNDBUTTON.
    @type index: number
    @param index: the index of imageview

    '''
    if not can_continue():
        return
    assert_type_string(view_type)
    assert_type_int(index)
    cmd = __generate_cmd_for_view_enabled(view_type, ID_TYPE_INDEX, index)
    result = interact_with_server(cmd)
    if result == BOOL_TRUE:
        return True
    elif result == BOOL_FALSE:
        return False

def __generate_cmd_for_view_enabled(view_type, id_type, _id, isVerticalList=1, isScrollable=1, searchFlag=TEXT_STARTS_WITH):

    if id_type == ID_TYPE_INDEX:
        cmd = generate_cmd(ACTION_GET_VIEW_ENABLED, view_type, id_type, str(_id), [])
    else :
        cmd = generate_cmd(ACTION_GET_VIEW_ENABLED, view_type, id_type, _id, [str(isVerticalList), str(isScrollable), searchFlag])
    return cmd

def __generate_cmd_for_view_text(view_type, id_type, _id, isVerticalList=1, isScrollable=1):

    if id_type == ID_TYPE_INDEX:
        cmd = generate_cmd(ACTION_GET_VIEW_TEXT, view_type, id_type, str(_id), [])
    else :
        cmd = generate_cmd(ACTION_GET_VIEW_TEXT, view_type, id_type, _id, [str(isVerticalList), str(isScrollable)])
    return cmd

def set_progressbar_by_index(index, value):
    '''
    set progressbar by index.

    @type index: number
    @param index: the index of progressbar
    @type value: string
    @param value: the value of progressbar

    '''
    if not can_continue():
        return
    assert_type_int(index)
    assert_type_string(value)
    cmd = generate_cmd(ACTION_SET_VALUE, VIEW_PROGRESSBAR, ID_TYPE_INDEX, str(index), [value])
    interact_with_server(cmd)

def search_view_by_id(_id):
    '''
    check whether exists view by id.

    @type _id: string
    @param _id: the id of view
    @return: True: exist; False: no.

    '''
    if not can_continue():
        return False
    assert_type_string(_id)
    cmd = generate_cmd(ACTION_SEARCH_VIEW, '', ID_TYPE_ID, _id, [])
    result = interact_with_server(cmd)
    if result == BOOL_TRUE:
        return True
    elif result == BOOL_FALSE:
        return False

def search_view_by_desc(desc):
    '''
    check whether exists view by description.

    @type desc: string
    @param desc: the description of view
    @return: True: exist; False: no.

    '''
    if not can_continue():
        return False
    assert_type_string(desc)
    cmd = generate_cmd(ACTION_SEARCH_VIEW, '', ID_TYPE_DESC, desc, [])
    result = interact_with_server(cmd)
    if result == BOOL_TRUE:
        return True
    elif result == BOOL_FALSE:
        return False

def is_external_storage_enable():
    '''
    check whether exists enable external storage.

    @return: True: exist; False: no.

    '''
    if not can_continue():
        return False
    cmd = generate_cmd(ACTION_CHECK_EXTERNAL_STORAGE, '', '', '', [])
    result = interact_with_server(cmd)
    if result == BOOL_TRUE:
        return True
    elif result == BOOL_FALSE:
        return False

def get_system_language():
    '''
    get current system language.

    @return: the system language.
    '''

    if not can_continue():
        return ''
    cmd = generate_cmd(ACTION_CHECK_SYSTEM_LANGUAGE, '', '', '', [])
    result = interact_with_server(cmd)
    return result

def get_activity_name():
    '''
    get current activity name.

    @return: current activity name.
    '''

    cmd = generate_cmd(ACTION_GET_ACTIVITY_NAME, '','', '', [])
    result = interact_with_server(cmd)
    return result

def click(x,y):
    '''
    click screen by coordinate point.

    @type x: number
    @param x: x-coordinate point.
    @type y: number
    @param y: y-coordinate point.

    '''
    if not can_continue():
        return ''
    #cmd = generate_cmd(ACTION_GET_ACTIVITY_NAME, '','', '', [str(x),str(y)])
    #log_test_framework(_LOG_TAG, 'send: ' + cmd)
    run_cmd("input  tap " + str(x) +" " + str(y))
    #log_test_framework(_LOG_TAG, 'receive: 1')
    #log_test_framework(_LOG_TAG, 'ok without result')

def wait_for_fun(fun,flag,timeout,sleeptime=1):
    '''
    It will loop the fun operation until the return value of fun is same with flag or wait time
    reaches the timeout. If fun success , wait_for_fun will return true , else will return false.

    @type fun: string
    @param fun: the fun operation.
    @type flag: boolean
    @param flag: expected flag value.
    @type timeout: number
    @param timeout: time out.
    @type sleeptime: number
    @param sleeptime: the seconds of sleep time.

    '''
    start_time = time.time()
    while int(time.time()) - int(start_time) < int(timeout):
        if fun() == flag:
            log_test_framework(_LOG_TAG,str(fun) + ' expected '+ str(flag))
            return True
        else:
            sleep(sleeptime)
    return False

#appName: application name.
#className: UI element name. eg: VIEW_PROGRESSBAR, VIEW_CHECKBOX and etc.
#idType: the category which id belongs to. eg: ID_TYPE_ID,ID_TYPE_TEXTS and etc.
#aciton: the type of action which will be performed when condition is matched. only support ACTION_CLICK and ACTION_GO_BACK
def register_update_watcher(appName, className, idType, id, action):
    '''
    register a watcher to deal with suddenly pop up  events in background.

    @type appName: string
    @param appName: application name.
    @type className: string
    @param className: UI element name. eg: VIEW_PROGRESSBAR, VIEW_CHECKBOX and etc.
    @type idType: string
    @param idType: the category which id belongs to. eg: ID_TYPE_ID,ID_TYPE_TEXTS and etc.
    @type id: string
    @param id: the id of the view.
    @type action: string
    @param action: the type of action which will be performed when condition is matched. only support ACTION_CLICK and ACTION_GO_BACK

    '''
    #if not can_continue():
    #    return
    assert_type_string(appName)
    assert_type_string(className)
    assert_type_string(idType)
    assert_type_string(id)
    assert_type_string(action)
    cmd = generate_cmd(ACTION_UPDATE_REGISTER, className, idType, id, [appName, action])
    interact_with_server(cmd)

def register_condition_action_watcher( packageName_condition,className_condition,idType_condition,id_condition,
    action,className_action,idType_action,id_action ):    
    '''
    register a watcher to deal with suddenly interrupt condition.
    The following 4 parameters define the interrupt condition:
        [ packageName_condition,  className_condition, idType_condition, id_condition] 
    The others parameters define how to do next after find the interrupt?
        [action,             className_action,    idType_action,    id_action]
    For example: check some special text for interrupt condition, 
    and click the ok_button close the interrupt.
    
    @type packageName_condition: string
    @param packageName_condition: package  name.
    @type className_condition/className_action: string
    @param className_condition/className_action: 
        UI element name. eg: VIEW_PROGRESSBAR, VIEW_CHECKBOX and etc.
    @type idType_condition/idType_action: string
    @param idType_condition / idType_action : 
        the category which id belongs to. eg: ID_TYPE_ID,ID_TYPE_TEXTS and etc.
    @type id_condition/id_action: string
    @param id_action/id_condition : the id of the view.
    @type action: string
    @param action: the type of action which will be performed when condition is matched. 
    current only support ACTION_CLICK,ACTION_GO_BACK and ACTION_LEFT_DRAG /ACTION_RIGHT_DRAG

    '''
    #if not can_continue():
    #    return
    assert_type_string(className_action)
    assert_type_string(idType_action)
    assert_type_string(id_action)
    assert_type_string(action)
    osInfo = get_platform_info()
    #if(osInfo == 'Linux-Phone'):
    if(osInfo == 'Linux-Phone' or osInfo == 'Windows'):
        cmd = generate_cmd(ACTION_WATCHER_REGISTER , className_condition, idType_condition, id_condition,[packageName_condition, action, className_action, idType_action, id_action])
        log_test_framework(_LOG_TAG, ' WATCHER condition REGISTER className ' + str(className_condition) )
        interact_with_server(cmd)

#appName: application name.

def unregister_update_watcher(appName):
    '''
    unregister the update watcher.

    @type appName: string
    @param appName: application name.

    '''
    if not can_continue():
        return
    assert_type_string(appName)
    cmd = generate_cmd(ACTION_UPDATE_UNREGISTER, '', '', '', [appName])
    interact_with_server(cmd)

#mode: should be ZOOM_DOWN/ZOOM_UP
def zoom_by_param(mode, startX1 = -1, startY1 = 1, startX2 = -1, startY2 = -1):
    '''
    zoom down or zoom up screen.

    @type mode: string
    @param mode: the mode of zoom,ZOOM_DOWN/ZOOM_UP
    @type startX1: Number
    @param startX1: start x-coordinate postion by percent
    @type startY1: Number
    @param startY1: start y-coordinate postion by percent
    @type startX2: Number
    @param startX2: end x-coordinate postion by percent
    @type startY2: Number
    @param startY2: end y-coordinate postion by percent

    '''
    if not can_continue():
        return
    assert_type_int(startX1)
    assert_type_int(startY1)
    assert_type_int(startX2)
    assert_type_int(startY2)
    assert_type_string(mode)
    cmd = generate_cmd(ACTION_ZOOM, '', '', '', [str(startX1), str(startY1), str(startX2), str(startY2), mode])
    interact_with_server(cmd)

def getDisplayWidth():
    '''
    get display width.

    @return: display width
    '''
    cmd = generate_cmd(ACTION_GET_DISPLAY_WIDTH, '', '', '', [])
    result = interact_with_server(cmd)
    return result

def getDisplayHeight():
    '''
    get display height.

    @return: display height
    '''
    cmd = generate_cmd(ACTION_GET_DISPLAY_HEIGHT, '', '', '', [])
    result = interact_with_server(cmd)
    return result

def save_reboot_status(suit_name, case_name):
    '''
    save reboot status into files before reboot.

    @type suit_name: string
    @param suit_name: the current suit name while QSST run.
    @type case_name: string
    @param case_name: the current case name while QSST run.

    '''
    qsst_log_reboot_manual()

def restore_reboot_status():
    '''
    remove previous reboot status files.

    '''
    qsst_log_restore_reboot()

def pause_python_process():
    '''
    pause python process.
    attention:this function can't use on windows system.

    '''
    def myHandler(signum, frame):
        restore_reboot_status()
        qsst_log_case_status(STATUS_FAILED, "Something wrong, the device should be rebooted.", SEVERITY_HIGH)

    signal.signal(signal.SIGALRM, myHandler)
    signal.alarm(WAIT_TIME)
    signal.pause()

def get_reboot_status(suit_name, case_name):
    '''
    get reboot status.

    @type suit_name: string
    @param suit_name: the current suit name.
    @type case_name: string
    @param case_name: the current case name.
    @return: True: reboot status, False:no.

    '''
    if is_suit_in_reboot_status(suit_name) and is_case_in_reboot_status(case_name):
        return True
    return False

#interval: set specific time (seconds) that device will wakeup.
#          default value is -1, means try to sleep device without register alarmer.
def goToSleepMode(interval = -1):
    '''
    go to sleep mode.

    @type interval: number
    @param interval: set specific time (seconds) that device will wakeup.
                      default value is -1, means try to sleep device without register alarmer.

    '''
    if not can_continue():
        return
    osInfo = get_platform_info()
    if(osInfo == 'Linux-Phone'):
        assert_type_int(interval)
        signal.signal(signal.SIGUSR1, wakeUpSignalHandler)
        cmd = generate_cmd(ACTION_SLEEP, '', '', '', [str(interval)])
        result = interact_with_server(cmd)
        if result == BOOL_FALSE:
            send_key(KEYCODE_POWER)
        if(interval > 0):
            signal.pause()

def wakeUpDevice():
    '''
    wake up device.

    '''
    if not can_continue():
        return
    osInfo = get_platform_info()
    if(osInfo == 'Linux-Phone'):
        cmd = generate_cmd(ACTION_WAKEUP, '', '', '', [])
        interact_with_qsst_server(cmd)

def unregisterAlarmer():
    '''
    finish the process of wake up device before time is up.

    '''
    osInfo = get_platform_info()
    if(osInfo == 'Linux-Phone'):
        cmd = generate_cmd(ACTION_ALARMER_UNREGISTER, '', '', '', [])
        interact_with_qsst_server(cmd)

def send_mms(smsto, content):
    '''
    send a mms to specific phone in background

    @type smsto: string
    @param smsto: the number of target phone.
    @type content: string
    @param content: the mms content.

    '''
    if not can_continue():
        return
    cmd = generate_cmd(ACTION_SEND_MMS, '', '', '', [smsto,content])
    interact_with_qsst_server(cmd)

def mt_trigger_service_call(to, wait_time, hold_time, interval, num_of_calls=1, count_off=True):
    '''
    trigger mt service for a mt call

    @type to: string
    @param to: specify the target phone number.
    @type wait_time: number
    @param wait_time: time for waiting to connect.
    @type hold_time: number
    @param hold_time: holding time for each call.
    @type interval: number
    @param interval: time between two calls, should be larger than < hold_time + wait_time  + 10>
    @type num_of_calls: number
    @param num_of_calls: how many calls want to make.
    @type count_off: boolean
    @param count_off: will speak out the current number of calls once specified true.

    '''
    if not can_continue():
        return
    cmd = generate_cmd(ACTION_MT_TRIGGER_SERVICE, '', '', '', ['MTCALL',str(count_off),str(interval),str(hold_time),to,str(wait_time),str(num_of_calls)])
    ret_value = interact_with_qsst_server(cmd)
    if ret_value == "null":
        return False
    return True

def mt_trigger_service_sms(msg_title_text, to, interval, time_out, count=1, msg_type=0, wap_url=" "):
    '''
    trigger mt service for a mt sms

    @type msg_title_text: string
    @param msg_title_text:This will be a body for SMS/WAP PUSH/FLASH SMS , and title for MMS.
    @type to: string
    @param to:Specify the target phone number.
    @type interval: number
    @param interval:Time between two consecutive SMS/MMS/WAP PUSH/FLASH SMS.
    @type time_out: number
    @param time_out: Server will abandon the request if it waits over this time.
    @type count: number
    @param count:How many SMS/MMS/WAP PUSH/FLASH SMS you want to make.
    @type msg_type: number
    @param msg_type: Select SMS type you want to send, SMS/MMS/WAP PUSH/FLASH SMS supported.0 for standard SMS, 1 for MMS, 2 for WAP PUSH, 3 for FLASH SMS.
    @type wap_url: string
    @param wap_url: URL for WAP PUSH, if it is SMS/MMS/FLASH SMS, leave it "".

    '''
    if not can_continue():
        return
    cmd = generate_cmd(ACTION_MT_TRIGGER_SERVICE, '', '', '', ['REQ_SMS',str(count),msg_title_text,str(interval),wap_url,to,str(time_out),str(msg_type)])
    ret_value = interact_with_qsst_server(cmd)
    if ret_value == "null":
        return False
    return True

def mt_trigger_service_email(to, subject, body, cc=" ", bcc=" ", count=1):
    '''
    trigger mt service for a mt email

    @type to: string
    @param to:Send MT Email to this address
    @type subject: string
    @param subject:Subject for the email.
    @type body: string
    @param body:Email body.
    @type cc: string
    @param cc:Cc address.
    @type bcc: string
    @param bcc:Bcc address.
    @type count: number
    @param count:How many emails you want to make.

    '''
    if not can_continue():
        return
    cmd = generate_cmd(ACTION_MT_TRIGGER_SERVICE, '', '', '', ['SEND_EMAIL',body,str(count),subject,to,cc,bcc])
    ret_value = interact_with_qsst_server(cmd)
    if ret_value == "null":
        return False
    return True

def enable_scroll_profling():
    '''
    just used for debug fps.

    '''
    if not can_continue():
        return
    cmd = generate_cmd(ACTION_ENABLE_SCROLL_PROFILING, '', '', '', [])
    interact_with_server(cmd)

def disable_scroll_profling():
    '''
    just used for debug fps.

    '''
    if not can_continue():
        return
    cmd = generate_cmd(ACTION_DISABLE_SCROLL_PROFILING, '', '', '', [])
    interact_with_server(cmd)

def get_postion():
    '''
    get postion of DUT.

    @return: the longitude and latitude.

    '''
    cmd = generate_cmd(ACTION_GET_POSTION, '', '', '', [])
    result = interact_with_qsst_server(cmd)
    return result

def get_speed():
    '''
    get speed of DUT.

    @return: the speed. unit is meter per second.

    '''
    cmd = generate_cmd(ACTION_GET_SPEED, '', '', '', [])
    result = interact_with_qsst_server(cmd)
    return result

#unit: the unit of battery temperate. eg: TEMP_UNIT_C,TEMP_UNIT_F.
def get_battery_temperate(unit=TEMP_UNIT_C):
    '''
    get temperate of battery.

    @type unit: string
    @param unit: the unit of battery temperate. TEMP_UNIT_C:Celsius; TEMP_UNIT_F:Fahrenheit.
    @return: the temperate.

    '''
    cmd = generate_cmd(ACTION_GET_BATTERY_TEMPERATE, '', '', '', [unit])
    result = interact_with_qsst_server(cmd)
    return result

#return value x,y,z
#x: Acceleration force along the x axis
#y: Acceleration force along the y axis
#z: Acceleration force along the z axis
def get_orientation():
    '''
    get orientation.

    @return: x,y,z.
             x: Acceleration force along the x axis
             y: Acceleration force along the y axis
             z: Acceleration force along the z axis.

    '''
    cmd = generate_cmd(ACTION_GET_ORIENTATION, '', '', '', [])
    result = interact_with_qsst_server(cmd)
    return result

def get_available_ram():
    '''
    get available RAM.

    @return: the available RAM. unit:M.

    '''
    cmd = generate_cmd(ACTION_GET_AVAILABLE_RAM, '', '', '', [])
    result = interact_with_qsst_server(cmd)
    return result

def get_available_rom():
    '''
    get available ROM.

    @return: the available ROM. unit:M.

    '''
    cmd = generate_cmd(ACTION_GET_AVAILABLE_ROM, '', '', '', [])
    result = interact_with_qsst_server(cmd)
    return result

def get_wifi_rssi():
    '''
    get wifi rssi.

    @return: the rssi of the wifi.
             SIGNAL_STRENGTH_NONE_OR_UNKNOWN: none or unknown signal strength.
             SIGNAL_STRENGTH_POOR: poor signal strength.
             SIGNAL_STRENGTH_MODERATE: moderate signal strength.
             SIGNAL_STRENGTH_GOOD: good signal strength.
             SIGNAL_STRENGTH_GREAT: great signal strength.

    '''
    cmd = generate_cmd(ACTION_GET_WIFI_RSSI, '', '', '', [])
    result = interact_with_qsst_server(cmd)
    rssi = {"0": SIGNAL_STRENGTH_NONE_OR_UNKNOWN, "1": SIGNAL_STRENGTH_POOR, "2": SIGNAL_STRENGTH_MODERATE, "3": SIGNAL_STRENGTH_GOOD, "4": SIGNAL_STRENGTH_GREAT}
    return rssi.get(result)

#slotId: sim card. eg: SLOT_ONE,SLOT_TWO.
def get_sim_card_state(slotId):
    '''
    get the state of the device SIM card in a slot.

    @type slotId: string
    @param slotId: the sim card. SLOT_ONE:slot1; SLOT_TWO:slot2.
    @return: the state of the device SIM card in the slot.
             SIM_STATE_ABSENT: SIM card state: no SIM card is available in the device.
             SIM_STATE_READY: SIM card state: Ready.
             SIM_STATE_DEACTIVATED: SIM card state: SIM Card Deactivated.
             SIM_STATE_UNKNOWN: SIM card state: SIM card is unknown or locked or error.
    '''
    cmd = generate_cmd(ACTION_GET_SIM_CARD_STATE, '', '', '', [slotId])
    result = interact_with_qsst_server(cmd)
    state = {"0": SIM_STATE_UNKNOWN, "1": SIM_STATE_ABSENT, "2": SIM_STATE_READY, "3": SIM_STATE_DEACTIVATED}
    return state.get(result)

#slotId: sim card. eg: SLOT_ONE,SLOT_TWO.
def get_sim_card_rssi(slotId):
    '''
    get the rssi of the device SIM card in a slot.

    @type slotId: string
    @param slotId: the sim card. SLOT_ONE:slot1; SLOT_TWO:slot2.
    @return: the rssi of the device SIM card in the slot.
             SIGNAL_STRENGTH_NONE_OR_UNKNOWN: none or unknown signal strength.
             SIGNAL_STRENGTH_POOR: poor signal strength.
             SIGNAL_STRENGTH_MODERATE: moderate signal strength.
             SIGNAL_STRENGTH_GOOD: good signal strength.
             SIGNAL_STRENGTH_GREAT: great signal strength.
    '''
    cmd = generate_cmd(ACTION_GET_SIM_CARD_RSSI, '', '', '', [slotId])
    result = interact_with_qsst_server(cmd)
    rssi = {"0": SIGNAL_STRENGTH_NONE_OR_UNKNOWN, "1": SIGNAL_STRENGTH_POOR, "2": SIGNAL_STRENGTH_MODERATE, "3": SIGNAL_STRENGTH_GOOD, "4": SIGNAL_STRENGTH_GREAT, "5": SIGNAL_STRENGTH_NONE_OR_UNKNOWN}
    return rssi.get(result)

def is_bluetooth_enabled():
    '''
    get the status of the bluetooth device.

    @return: the status of the bluetooth device.
             True: enabled
             False: disabled.
    '''
    cmd = generate_cmd(ACTION_CHECK_BLUETOOTH, '', '', '', '')
    result = interact_with_qsst_server(cmd)
    if result == "true":
        return True
    else:
        return False

def is_wifi_enabled():
    '''
    get the status of the wifi.

    @return: the status of the wifi.
             True: enabled
             False: disabled.
    '''
    cmd = generate_cmd(ACTION_CHECK_WIFI, '', '', '', '')
    result = interact_with_qsst_server(cmd)
    if result == "true":
        return True
    else:
        return False

#slotId: sim card. eg: SLOT_ONE,SLOT_TWO.
def get_networktype(slotId):
    '''
    get the network type of the device SIM card in a slot.

    @type slotId: string
    @param slotId: the sim card. SLOT_ONE:slot1; SLOT_TWO:slot2.
    @return: the network type of the device SIM card in the slot.
              "CDMA": Includes: CDMA-IS95A, CDMA-IS95B, 1xRTT.
              "EVDO": Includes: EvDo-rev.0, EvDo-rev.A, EvDo-rev.B, eHRPD.
              "GSM": Includes: GPRS.
              "EDGE": Includes: EDGE.
              "H": Includes: HSDPA, HSUPA, HSPA, HSPA+.
              "UMTS": Includes: UMTS.
              "LTE": Includes: LTE.
              "UNKNOWN": Network type is Unknown.
    '''
    cmd = generate_cmd(ACTION_GET_NETWORKTYPE, '', '', '', [slotId])
    result = interact_with_qsst_server(cmd)
    return result

#inner use: combine cmd.
def get_logcat_cmd(tag,type,raw_cmd):
    '''
    combine command by params

    @type tag: string
    @param tag: the tag of logcat.
    @type type: string
    @param type: the log buffer of logcat.
    @type raw_cmd: string
    @param raw_cmd: the raw command.
    @return: combined command.

    '''
    if(raw_cmd == ""):
        cmd_tag = ""
        if(tag != ""):
            cmd_tag = " -s " + tag+":v "

        cmd_type = ""
        if(type != ""):
            for i in type.split(','):
                cmd_type = cmd_type + " -b " + i
        cmd = cmd_type + cmd_tag
    else:
        cmd = raw_cmd.replace('-d',' ')

    return cmd

#tag: logcat tag, can be empty
#type: log buffer, can be system,main,radio,events. such as system or system,radio.
#raw_cmd: when raw_cmd is not null, the tag and type are ignored
def get_logcat_stream(tag='', type='', raw_cmd=''):
    '''
    get logcat stream in case.

    @type tag: string
    @param tag: the tag of logcat,can be empty.
    @type type: string
    @param type: the log buffer of logcat,can be system,main,radio,events. such as system or system,radio.
    @type raw_cmd: string
    @param raw_cmd: the raw command.when raw_cmd is not null, the tag and type are ignored.
    @return: logcat stream.

    '''
    cmd = get_logcat_cmd(tag,type,raw_cmd)
    osInfo = get_platform_info()
    try:
        if(osInfo == 'Linux-Phone'):
            pipe = Popen("logcat " + cmd,stdout=PIPE,shell=True,executable='sh',bufsize=1)
        elif(osInfo == 'Linux-PC' or osInfo =='Windows'):
            pipe = Popen("adb logcat " + cmd,stdout=PIPE,bufsize=1)
    except Exception as e:
        log_test_framework(_LOG_TAG, "get_logcat_stream error"+str(e))
    return pipe

def get_logcat_string(tag='', type='', raw_cmd=''):
    '''
    get logcat string in case.

    @type tag: string
    @param tag: the tag of logcat,can be empty.
    @type type: string
    @param type: the log buffer of logcat,can be system,main,radio,events. such as system or system,radio.
    @type raw_cmd: string
    @param raw_cmd: the raw command.when raw_cmd is not null, the tag and type are ignored.
    @return: logcat result string

    '''
    logcat_string = ""
    osInfo = get_platform_info()
    cmd = get_logcat_cmd(tag,type,raw_cmd)
    if(osInfo == 'Linux-Phone'):
        cmd = 'logcat -d ' + cmd
    elif(osInfo == 'Linux-PC' or osInfo =='Windows'):
        cmd = 'adb logcat -d ' + cmd
    try:
        pipe = os.popen(cmd)
        logcat_string = pipe.read()
    except Exception as e:
        log_test_framework(_LOG_TAG, "get_logcat_string error"+str(e))
    return logcat_string

def kill_pipe(pipe):
    '''
    kill pipe

    @type pipe: string
    @param pipe: the pipe need to kill

    '''
    #pipe.stdout.close()
    pipe.kill()

def update_notificationbar(text):
    '''
    show progress on notificationbar when qsst is running.
    note:this api not support on PC

    @type tag: string
    @param tag: text that show on notification.

    '''
    if not can_continue():
        return
    cmd = generate_cmd(ACTION_UPDATE_NOTIFICATION, '', '', '', [text])
    interact_with_qsst_server(cmd)
