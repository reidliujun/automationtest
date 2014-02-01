#coding=utf-8
'''
   provide some interface of mms application.

   This class will provide operations api of mms application.

   1.Developer can directly call those api to perform some operation.

   2.Developer can add some new api.


   @author: U{c_chuanc<c_chuanc@qti.qualcomm.com>}
   @version: version 1.0.0
   @requires: python 2.7+
   @license:

   @see: L{Base <Base>}
   @note:
   @attention:
   @bug:
   @warning:



'''
from case_utility import *
from qrd_shared.Base import Base
from qrd_shared.ime.IME import IME
from logging_wrapper import log_test_framework
import settings.common as SC
from qrd_shared.camera.Camera import Camera

camera = Camera()

class Mms(Base):
    '''
    Mms is a class for operating Mms application.

    @see: L{Base <Base>}
    '''
    
    TAG = "Mms"
    '''@var TAG: tag of Mms'''
    def __init__(self):
        '''
        init function.
        '''
        self.mode_name = "mms"
        self.ime = IME()
        Base.__init__(self,self.mode_name)
        self.debug_print( 'Mms init:%f' %(time.time()))

    def click_home_icon(self):
        '''
        click home icon.

        @return: true-if click success.false-if click failed.
        '''
        if wait_for_fun(lambda:search_view_by_id("home"), True, 10):
            click_imageview_by_id("home")
            return True
        log_test_framework(self.TAG, "Can't search view 'home'.")
        return False

    def delete_all_threads(self):
        '''
        delete all threads.
        '''
        send_key(KEY_MENU)
        delete_all_threads = self.get_value("delete_all_threads")
        if search_text(delete_all_threads):
            click_textview_by_text(delete_all_threads)
            click_button_by_index(1)
            wait_for_fun(lambda:search_text(self.get_value("no_conversations")), True, 5)
        else:
            goback()

    # def send_sms(self, send_slot_number, recive_phone_number, content):
        # '''
        # use slot1 or slot2 to send a sms to a specific phone number,then check whether send success.

        # @type send_slot_number: number
        # @param send_slot_number: send slot,1-slot1,2-slot2
        # @type recive_phone_number: number
        # @param recive_phone_number: the phone nunber that recive the message.
        # @type content: string
        # @param content: text message.
        # @return: true-if send success,false-if send failed.
        # '''
        # num = recive_phone_number
        # mms_text = content
        # click_imageview_by_id('action_compose_new')
        # click_textview_by_id("recipients_editor")
        # self.ime.IME_input_number(1, num, "c")
        # click_textview_by_text(self.get_value("type_message"))
        # self.ime.IME_input_english(1, mms_text)
        # click_imageview_by_id('send_button_sms')
        # click_button_by_index(send_slot_number - 1)
        # func = lambda:search_text(self.get_value("sent"), searchFlag=TEXT_CONTAINS)
        # if wait_for_fun(func, True, 30):
            # self.click_home_icon()
            # return True
        # self.click_home_icon()
        # return False
    
    def sms(self, sms_num, slot, sms_text):
        click_imageview_by_index(0)
        sleep(2)
        send_key(KEY_MENU)
        delete_all_threads = self.get_value("delete_all_threads")
        if wait_for_fun(lambda:search_text(delete_all_threads), True, 3):
            click_textview_by_text(delete_all_threads)
            click_button_by_index(1)
            wait_for_fun(lambda:search_text(self.get_value("no_conversations")), True, 5)
        else:
            goback()
        click_imageview_by_id('action_compose_new')
#        entertext_edittext_by_id("recipients_editor", sms_num)
        time.sleep(1)
        osInfo = get_platform_info()
        if(osInfo == "Windows" or osInfo == "Linux-PC"):
            subprocess.Popen(["adb", "shell", "input text " + sms_num])
        elif(osInfo == "Linux-Phone"):
            os.system("input text " + sms_num)
        #os.system("input text " + sms_num)
        click_imageview_by_id('recipients_editor')
        entertext_edittext_by_id("embedded_text_editor", sms_text)
        click_imageview_by_id('send_button_sms')
        if SC.PUBLIC_DSDS:
            if slot == 0:
                click_button_by_index(0)
            else:
                click_button_by_index(1)

        func = lambda:search_text(self.get_value("sent"), searchFlag=TEXT_CONTAINS)
        if wait_for_fun(func, True, 15):
            return True
        else:
            return False
        click_imageview_by_index(0)

    def mms(self, mms_num, slot, mms_text):
        click_imageview_by_index(0)
        sleep(2)
        send_key(KEY_MENU)
        delete_all_threads = self.get_value("delete_all_threads")
        if wait_for_fun(lambda:search_text(delete_all_threads), True, 3):
            click_textview_by_text(delete_all_threads)
            click_button_by_index(1)
            wait_for_fun(lambda:search_text(self.get_value("no_conversations")), True, 5)
        else:
            goback()
        click_imageview_by_id('action_compose_new')
#        entertext_edittext_by_index(0, mms_num)
        time.sleep(1)
        osInfo = get_platform_info()
        if(osInfo == "Windows" or osInfo == "Linux-PC"):
            subprocess.Popen(["adb", "shell", "input text " + mms_num])
        elif(osInfo == "Linux-Phone"):
            os.system("input text " + mms_num)
        
        click_textview_by_desc(self.get_value("attach"))
        click_textview_by_text(self.get_value("capture_picture"))
        if search_view_by_id("alertTitle"):
            click_imageview_by_index(0)
            click_button_by_id("button_always")
        if search_view_by_id("message"):
            click_button_by_id("button2")
        camera.get_picture_by_camera()
        entertext_edittext_by_index(1, mms_text)
        click_textview_by_id("send_button_mms")
#        if SC.PUBLIC_DSDS:
#            click_button_by_index(0)
        if SC.PUBLIC_DSDS:
            if slot == 0:
                click_button_by_index(0)
            else:
                click_button_by_index(1)
        
        func = lambda:search_text(self.get_value("sent"), searchFlag=TEXT_CONTAINS)
        if wait_for_fun(func, True, 180):
            return True
        else:
            return False
        click_imageview_by_index(1)
        
    def mtsms(self,sms_num,sms_text,sms_repeat_times,intervaltime):
        click_textview_by_text("MT SMS/MMS")
        click_textview_by_text("Add")
        entertext_edittext_by_index(0,sms_num)
        click_textview_by_text("Ok")
        entertext_edittext_by_index(1,sms_text)
        goback()
        entertext_edittext_by_index(3,sms_repeat_times)
        entertext_edittext_by_index(4,intervaltime)
        goback()
        click_textview_by_text("Send")
        sleep(15)
    def mtsms_multislot(self,sms_num1,sms_num2,sms_text,sms_repeat_times,intervaltime):
        click_textview_by_text("MT SMS/MMS")
        click_textview_by_text("Add")
        entertext_edittext_by_index(0,sms_num1)
        entertext_edittext_by_index(1,sms_num2)
        click_textview_by_text("Ok")
        entertext_edittext_by_index(1,sms_text)
        goback()
        entertext_edittext_by_index(3,sms_repeat_times)
        entertext_edittext_by_index(4,intervaltime)
        goback()
        click_textview_by_text("Send")
        sleep(15)
    def mtmms(self,mms_num,mms_text,mms_repeat_times,mms_attachment,intervaltime):
        click_textview_by_text("MT SMS/MMS")
        click_button_by_index(1)
        
        click_textview_by_text("Add")
        entertext_edittext_by_index(0,mms_num)
        click_textview_by_text("Ok")
        entertext_edittext_by_index(1,mms_text)
        goback()
        click_textview_by_index(14)
        click_textview_by_text(mms_attachment)
        
        entertext_edittext_by_index(3,mms_repeat_times)
        entertext_edittext_by_index(4,intervaltime)
        goback()
        click_textview_by_text("Send")
        sleep(20)
