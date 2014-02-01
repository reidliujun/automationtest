#coding=utf-8
from case_utility import *
from qrd_shared.Base import Base
from qrd_shared.language.language import Language
import time
from qrd_shared.ime.IME import IME
############################################
#author:
#    lihuang@cienet.com.cn
#function:
#    the browser mode of qrd share lib.
#doc:
############################################
class Browser(Base):

    def __init__(self):
        self.mode_name = "browser"
        Base.__init__(self,self.mode_name)
        self.debug_print( 'Base init:%f' %(time.time()))

    #check whether access url successfully
    #url_address: url address
    #check_vlaue: when need check whether access successfully, this is the check value
    #wait_time: when check access , the wait time
    #is_checked: whether check to access successfully
    def access_browser(self, url_address, check_value, wait_time, is_checked=True):
        search_result = False
        ime = IME()

#        if is_checked == True:
#            #clear the browser cache
#            self.clear_cache()

        #addressing config web address
        click_textview_by_id("url")
        send_key(KEY_DEL)
        #input address url
#        ime.IME_input(1,url_address)
        entertext_edittext_by_id("url",url_address)
        click(650,1250)
        #make sure whether access successful
        if is_checked == True:
            scroll_down()
            wait_fun = lambda: search_view_by_id("favicon")
            wait_result = wait_for_fun(wait_fun,True,wait_time)

            if wait_result == True:

                start_time = time.time()
                while time.time() - start_time < wait_time:
                    click_button_by_id("favicon")
                    if search_text(unicode(check_value)):
                        search_result =  True
                        break
                    elif search_text(self.get_value("webpage_not_available")):
                        search_result =  False
                        break
                    else:
                        sleep(1)
                    goback()
            else:
                search_result =  False
        else:
            if search_text(url_address):
                search_result =  True
            else:
                search_result =  False

        return search_result

    def clear_cache(self):
        #clear the browser cache
        click_menuitem_by_text(self.get_value("menu_preferences"))
        click_textview_by_text(self.get_value("pref_privacy_security_title"))
        click_textview_by_text(self.get_value("pref_privacy_clear_cache"))

        if search_text(self.get_value("dialog_ok_button")):
            click_button_by_text(self.get_value("dialog_ok_button"))

        goback()
        goback()

    #check google account automatic signing
    #check connection problem
    def pre_check(self):
        sleep(1)

        #check google account automatic signing
        if search_text(self.get_value("google_account_auto_connection"),1,0) == True:
            goback()

        #check connection problem
        if search_text(self.get_value("Connection_problem"),1,0) == True:
            goback()
            
    def browsing(self,address,wait,web_title_1,web_title_2):

        #clear browser cache
        click_menuitem_by_text(self.get_value("menu_preferences"))
        click_textview_by_text(self.get_value("pref_privacy_security_title"))
        click_textview_by_text(self.get_value("pref_privacy_clear_cache"))

        if search_text(self.get_value("dialog_ok_button")):
            click_button_by_text(self.get_value("dialog_ok_button"))

        goback()
        goback()
        sleep(3)
        scroll_to_top()

        #addressing config web address
        click_textview_by_id("url")
        send_key(KEY_DEL)
        #input address url
        entertext_edittext_by_id("url",address)
        #ime.IME_input(1,SC.PRIVATE_BROWSER_ADDRESS_URL_SEQUENCE)
        click(650,1250)

        sleep(wait)
        scroll_to_top()
        if not search_view_by_id("favicon"):
            search_result_1 = False
        else:
            click_button_by_id("favicon")
            if search_text(unicode(web_title_1),isScrollable=0):
                search_result_1 =  True
            else:
                search_result_1 =  False
            goback()
        click(80,200)

        sleep(wait)
        
        scroll_to_top()
        if not search_view_by_id("favicon"):
            search_result_2 = False
        else:
            click_button_by_id("favicon")
            #sleep(1)
            #click_button_by_id("favicon")
            if search_text(unicode(web_title_2),isScrollable=0):
                search_result_2 =  True
            else:
                search_result_2 =  False
            goback()

        send_key(KEY_HOME)

        #result
        if search_result_1 == True and search_result_2 == True:
            return True
        else:
            return False
        
        sleep(2)