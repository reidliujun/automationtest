#coding=utf-8
'''
   provide some interface of settings application.

   This class will provide operations api of settings application.

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
import settings.common as SC
from qrd_shared.Base import Base
from qrd_shared.ime.IME import IME
from logging_wrapper import log_test_framework
import time

class Settings(Base):
    '''
    Settings is a class for operating Settings application.

    @see: L{Base <Base>}
    '''
    TAG = "Settings"
    '''@var TAG: tag of Settings'''
    global count
    count = 0
    '''@var count: count login,init value is 0'''
    def __init__(self):
        '''
        init method.
        '''
        self.mode_name = "settings"
        Base.__init__(self,self.mode_name)
        self.ime = IME()
        self.debug_print( 'Settings init:%f' %(time.time()))

    def close_lockscreen(self):
        '''
        set screen lock as None.
        set screen sleep as Never.
        '''
        time.sleep(1)
        scroll_up()
        click_textview_by_text(self.get_value("security"))
        click_textview_by_text(self.get_value("screen_lock"))
        time.sleep(1)
        click_textview_by_text(self.get_value("none"))
        time.sleep(1)
        click_imageview_by_index(0)

        time.sleep(1)
        scroll_up()
        click_textview_by_text(self.get_value("display"))
        if is_checkbox_checked_by_index(0):
            click_checkbox_by_index(0)
        click_textview_by_text(self.get_value("sleep"))
        time.sleep(1)
        click_textview_by_text(self.get_value("never"))
        time.sleep(1)
        click_imageview_by_index(0)

    def select_language(self, lan):
        '''
        set system language.

        @type lan:string
        @param lan:: language name
        '''
        click_textview_by_index(19)
        click_textview_by_index(1)
        sleep(1)
        click_textview_by_text(lan)
        sleep(2)
        click_imageview_by_index(0)

    def enable_wifi(self, wifi_name, wifi_pwd):
        '''
        enable wifi.

        @type wifi_name: string
        @param wifi_name: wifi name
        @type wifi_pwd: tuple
        @param wifi_pwd: wifi password
        @return: whether enable wifi success
        '''
        click_textview_by_text(self.get_value("wifi"))
        if search_text(self.get_value("see_available_networks"), searchFlag=TEXT_CONTAINS):
            click_button_by_index(0)
            sleep(10)
        sleep(5)
        #scroll_down()
        if not search_text(wifi_name):
            click_imageview_by_index(0)
            return False
        click_textview_by_text(wifi_name)
        flag_wifi = 0
        if not wifi_pwd == "":
            if search_view_by_id("password"):
                #entertext_edittext_by_index(0, wifi_pwd)
                click_textview_by_id("password")
                self.ime.IME_input(1, wifi_pwd)
                click_button_by_text(self.get_value("connect"))
            elif search_text(self.get_value("connected")):
                flag_wifi = 1
                goback()
            elif search_text(self.get_value("forget")) and search_text(self.get_value("connect")):
                click_button_by_text(self.get_value("connect"))
            else:
                log_test_framework(self.TAG, "something wrong after click wifi name.")
                goback()
                click_imageview_by_index(0)
                return False
        else:
            if search_text(self.get_value("forget")):
                goback()
        if flag_wifi == 1:
            click_imageview_by_index(0)
            return True
        sleep(10)
        click_textview_by_text(wifi_name)
        if search_text(self.get_value("connected")):
            goback()
            click_imageview_by_index(0)
            return True
        else:
            goback()
            click_imageview_by_index(0)
            return False
    def setting_hotspot(self):
        '''
        enable hotspot
        '''
        click_textview_by_text(self.get_value("more"))
        click_textview_by_text(self.get_value("tethering portable hotspot"))
        click_textview_by_text(self.get_value("portable wlan hotspot"))

    def disable_wifi(self):
        '''
        disable wifi.
        '''
        #click_textview_by_text(self.get_value("wifi"))
#        if not search_text(self.get_value("see_available_networks"), searchFlag=TEXT_CONTAINS):
#            click_button_by_index(0)
#        click_imageview_by_index(0)
        if is_compoundbutton_checked_by_index(0):
            click_button_by_index(0)
    
    def enable_bluetooth(self):
        click_textview_by_text(self.get_value("bluetooth"))
        if search_text(self.get_value("see_devices"), searchFlag=TEXT_CONTAINS):
            click_button_by_index(0)
            sleep(10)
            sleep(5)
        else:
            goback()
            click_imageview_by_index(0)
        return False
    
    def disable_bluetooth(self):
        click_textview_by_text(self.get_value("bluetooth"))
        if not search_text(self.get_value("see_devices"), searchFlag=TEXT_CONTAINS):
            click_button_by_index(0)
            sleep(10)
            sleep(5)
        else:
            goback()
            click_imageview_by_index(0)
        return False
    
    def access_cmwap(self):
        '''
        set access point to cmwap
        '''
        click_textview_by_text(self.get_value("more"))
        click_textview_by_text(self.get_value("mobile networks"))
        click_textview_by_text(self.get_value("access point names"))
        click_button_by_index(1)
        
    def access_cmnet(self):
        '''
        set access point to cmnet
        '''
        click_textview_by_text(self.get_value("more"))
        click_textview_by_text(self.get_value("mobile networks"))
        click_textview_by_text(self.get_value("access point names"))
        click_button_by_index(0)

    def add_google_account(self, user_name, user_pwd):
        '''
        add google account.

        @type user_name: string
        @param user_name: google account name
        @type user_pwd: tuple
        @param user_pwd: google account password
        @return: whether add google account success
        '''
        click_textview_by_text(self.get_value("add_account"))
        click_textview_by_text("Google")
        click_button_by_id("next_button")
        #entertext_edittext_by_id("username_edit", user_name)
        click_textview_by_id("username_edit")
        self.ime.IME_input(1, user_name)
        #entertext_edittext_by_id("password_edit", user_pwd)
        click_textview_by_id("password_edit")
        self.ime.IME_input(1, user_pwd)
        if search_text(self.get_value("keep_me_up"), searchFlag=TEXT_CONTAINS):
            click_button_by_id("button1")
        if search_text(self.get_value("account_exsits"), searchFlag=TEXT_CONTAINS):
            log_test_framework(self.TAG, "Account already exists.")
            click_button_by_id("next_button")
            start_activity("com.android.settings", ".Settings")
            return True
        #click_button_by_id("next_button")
        if not self.re_sign_in():
            log_test_framework(self.TAG, "Couldn't sign in.")
            return False
        if search_text(self.get_value("entertainment"), searchFlag=TEXT_CONTAINS):
            click_button_by_id("skip_button")
        click_button_by_id("done_button")
        return True

    def re_sign_in(self):
        '''
        if could not sign in,sign in continuous for 3 times

        @return: whether sign in success
        '''
        flag = True
        global count
        while(flag):
            if not search_text(self.get_value("signing_in"), searchFlag=TEXT_CONTAINS):
                flag = False
        if search_text(self.get_value("could_not_sign_in"), searchFlag=TEXT_CONTAINS):
            click_button_by_id("next_button")
            click_textview_by_text(self.get_value("next"))
            count += 1
            if count == 3:
                count = 0
                return False
            self.re_sign_in()
        else:
            count = 0
            return True

    def whether_open_gps(self, open):
        '''
        open or close gps.

        @type open: boolean
        @param open: true-open gps,false-close gps
        '''
        click_textview_by_text(self.get_value("location_access"))
        if open:
            if not is_compoundbutton_checked_by_index(0):
                click_button_by_index(0)
                fun = lambda:search_view_by_id("button2")
                if wait_for_fun(fun,True,2):
                    click_button_by_id("button2")
            else:
                if not is_checkbox_checked_by_index(0):
                    click_checkbox_by_index(0)
        else:
            if is_compoundbutton_checked_by_index(0):
                if is_checkbox_checked_by_index(0):
                    click_checkbox_by_index(0)
        click_imageview_by_index(0)

    def whether_open_mobile_data(self, open):
        '''
        open or close mobile data.

        @type open: boolean
        @param open: true-open mobile data,false-close mobile data
        '''
        if open:
            if not is_compoundbutton_checked_by_index(1):
                click_button_by_index(1)
        else:
            if is_compoundbutton_checked_by_index(1):
                click_button_by_index(1)

    def set_default_voice(self, card_id):
        '''
        set default voice.

        @type card_id: string
        @param card_id: default voice card id, 1-slot1, 2-slot2, 0-always ask
        '''
        click_textview_by_text(self.get_value("dual_sim_settings"))
        click_textview_by_text(self.get_value("voice"))
        if card_id == 0:
            click_in_list_by_index(2)
        elif card_id == 1:
            click_in_list_by_index(0)
        elif card_id == 2:
            click_in_list_by_index(1)
        else:
            log_test_framework(self.TAG, "card_id:" + card_id + "is error.")
        click_imageview_by_index(0)

    def set_default_data(self, card_id):
        '''
        set default data.

        @type card_id: string
        @param card_id: default data card id, 1-slot1, 2-slot2, 0-always ask
        '''
        click_textview_by_text(self.get_value("multi_sim_settings"))
        click_textview_by_text(self.get_value("data_call"))
        if card_id == 0:
            click_in_list_by_index(2)
        elif card_id == 1:
            click_in_list_by_index(0)
        elif card_id == 2:
            click_in_list_by_index(1)
        else:
            log_test_framework(self.TAG, "card_id:" + card_id + "is error.")

        fun = lambda:search_text(self.get_value("set_dds_success"))
        wait_for_fun(fun,False,20)

    def set_default_sms(self, card_id):
        '''
        set default sms.

        @type card_id: string
        @param card_id: default sms card id, 1-slot1, 2-slot2, 0-always ask
        '''
        click_textview_by_text(self.get_value("dual_sim_settings"))
        click_textview_by_text(self.get_value("sms"))
        if card_id == 0:
            click_in_list_by_index(2)
        elif card_id == 1:
            click_in_list_by_index(0)
        elif card_id == 2:
            click_in_list_by_index(1)
        else:
            log_test_framework(self.TAG, "card_id:" + card_id + "is error.")
        click_imageview_by_index(0)

    def is_wifi_connected(self, wifi_name):
        '''
        get wifi status whether wifi is connected.

        @type wifi_name: string
        @param wifi_name: wifi name
        @return: true-if wifi_name have connected, false-if wifi_name haven't connected
        '''
        click_textview_by_text(self.get_value("wifi"))
        if search_text(self.get_value("see_available_networks"), searchFlag=TEXT_CONTAINS):
            return False
        click_textview_by_text(wifi_name)
        if not search_text(self.get_value("connected")):
            return False
        return True
    
    def set_plmnsearch(self, card_id,time_after_search):
        if SC.PUBLIC_DSDS:
            click_textview_by_text(self.get_value("dual_sim_settings"))
            if card_id==0:
                click_textview_by_text(self.get_value("slot1_in_dual_sim"))
            else:
                click_textview_by_text(self.get_value("slot2_in_dual_sim"))
    #        if card_id==1:
    #            click_textview_by_text(self.get_value("slot2"))
            click_textview_by_text(self.get_value("mobile_network_settings"))
            click_textview_by_text(self.get_value("network_operators"))
            click_textview_by_text(self.get_value("search"))
            click_textview_by_text(self.get_value("ok"))
        else:
            click_textview_by_text(self.get_value("more"))
            click_textview_by_text(self.get_value("mobile_network_settings"))
            click_textview_by_text(self.get_value("network_operators"))
        fun = lambda:search_text(self.get_value("china"))
        if wait_for_fun(fun,True,time_after_search):
            return True
        else:
            return False
        take_screenshot()
        
    def switch_network(self, time_after_switch):
        click_textview_by_text(self.get_value("more"))
        click_textview_by_text(self.get_value("mobile_network_settings"))
        click_textview_by_text(self.get_value("network_mode"))
        click_textview_by_text(self.get_value("GSM/WCDMA/LTE"), searchFlag=TEXT_MATCHES)
        sleep(time_after_switch)
        click_textview_by_text(self.get_value("network_mode"))
        click_textview_by_text(self.get_value("GSM/WCDMA_preferred"), searchFlag=TEXT_MATCHES)

    def set_airplane(self,time_after_on,time_after_off):
        '''
        turn on and turn off airplane mode.
        '''
        click_textview_by_text(self.get_value("more"))
        if is_checkbox_checked_by_index(0):
            click_textview_by_text(self.get_value("airplane_mode"))
            sleep(time_after_off)
        else:
            click_textview_by_text(self.get_value("airplane_mode"))
            sleep(time_after_on)
            click_textview_by_text(self.get_value("airplane_mode"))
            sleep(time_after_off)
        if is_checkbox_checked_by_index(0):
            return False
        else:
            return True

    def turn_on_airplane(self,time_after_on,time_after_off):
        '''
        turn on airplane mode.
        '''
        click_textview_by_text(self.get_value("more"))
        if is_checkbox_checked_by_index(0):
            click_textview_by_text(self.get_value("airplane_mode"))
            sleep(time_after_off)
            click_textview_by_text(self.get_value("airplane_mode"))
            sleep(time_after_on)
        else:
            click_textview_by_text(self.get_value("airplane_mode"))
            sleep(time_after_on)
        if is_checkbox_checked_by_index(0):
            return True
        else:
            return False
        
    def turn_off_airplane(self,time_after_off):
        '''
        turn off airplane mode.
        '''
        click_textview_by_text(self.get_value("more"))
        if is_checkbox_checked_by_index(0):
            click_textview_by_text(self.get_value("airplane_mode"))
            sleep(time_after_off)

    def set_dds(self,wait):
        click_textview_by_text(self.get_value("data_call"))
        click_textview_by_text(self.get_value("slot2"))
        fun = lambda:search_text(self.get_value("set_dds_success"))
        wait_for_fun(fun,True,wait)
        take_screenshot()
        
        click_textview_by_text(self.get_value("data_call"))
        click_textview_by_text(self.get_value("slot1"))
        wait_for_fun(fun,True,wait)
        take_screenshot()
        
    def interRAT(self):
        click_textview_by_text(self.get_value("mobile_data"))

        if is_checkbox_checked_by_index(0):
            click_button_by_index(0)
#             print 'already on'
            sleep(120)
        else:
            click_button_by_index(0)
            sleep(60)
            click_button_by_index(0)
            sleep(120)
            
    def enableDATA(self):
        if SC.PUBLIC_DSDS:
            if not is_compoundbutton_checked_by_index(1):
                click_button_by_index(1)
                sleep(30)
        else:
            click_textview_by_text(self.get_value("more"))
            click_textview_by_text(self.get_value("mobile_network_settings"))
            if not is_compoundbutton_checked_by_index(0):
                click_button_by_index(0)
                sleep(30)

    def disableDATA(self):
        if SC.PUBLIC_DSDS:
            if is_compoundbutton_checked_by_index(1):
                click_button_by_index(1)
                sleep(30)
        else:
            click_textview_by_text(self.get_value("more"))
            click_textview_by_text(self.get_value("mobile_network_settings"))
            if is_compoundbutton_checked_by_index(0):
                click_button_by_index(0)
                sleep(30)

                
    def choose_default_language(self):
        click_textview_by_text(self.get_value("language"))
        click_textview_by_text(self.get_value("default"))
        if wait_for_fun(lambda:search_text(self.get_value("choose_input")), True, 5):
            click_textview_by_text(self.get_value("english"))
            goback()
            return True
        else:
            goback()
            return False
