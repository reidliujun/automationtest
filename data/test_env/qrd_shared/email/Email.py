from case_utility import *
from qrd_shared.Base import Base
from qrd_shared.language.language import Language
import time
from qrd_shared.case import *
from qrd_shared.ime.IME import IME
############################################
#author:
#    lihuang@cienet.com.cn
#function:
#    the email mode of qrd share lib.
#doc:
############################################
class Email(Base):

    def __init__(self):
        self.mode_name = "email"
        Base.__init__(self,self.mode_name)
        self.debug_print( 'Base init:%f' %(time.time()))

    #add an email account
    def add_email_account(self, user_name, user_pwd):
        #Add Email Account
        ime = IME()
        start_activity('com.android.settings','.Settings')

        scroll_to_bottom()
        click_textview_by_text(self.get_value("add_account_label"),1,0)
        click_textview_by_text(self.get_value("app_email"),1,0)

        #input account
        entertext_edittext_by_id("account_email",user_name)
#        click_textview_by_id("account_email",1,0)
#        ime.IME_input(1,user_name)

        #input password
#        ime.IME_input(1,user_pwd)
        entertext_edittext_by_id("account_password",user_pwd)
        #entertext_edittext_by_id("account_password",SC.PRIVATE_EMAIL_EMAIL_PASSWORD,1,0)

        sleep(1)
        click_button_by_id("next",1,0)
        click_button_by_id("pop",1,0)

        scroll_to_bottom()
        click_button_by_id("next",1,0)

        if not search_text(self.get_value("account_duplicate_dlg_title"),1,0):
            time = 0

            while (search_text(self.get_value("account_setup_check_settings_check_incoming_msg"),1,0) or search_text(self.get_value("could_not_open_connection"),1,0)) and time < 3:
                sleep(2)
                if search_text(self.get_value("could_not_open_connection"),1,0):
                    goback()
                    time = time + 1
                    click_button_by_id("next",1,0)

            if time == 3:
                return False
            else:
                click_imageview_by_id("account_security_type",1,0)
                click_textview_by_text(self.get_value("ssl_tls"),1,0)
                scroll_to_bottom()
                click_button_by_id("next",1,0)

                time = 0
                while (search_text(self.get_value("account_setup_check_settings_check_outgoing_msg"),1,0) or search_text(self.get_value("could_not_open_connection"),1,0)) and time < 3:
                    sleep(3)
                    if search_text(self.get_value("could_not_open_connection"),1,0):
                        goback()
                        time = time + 1
                        click_button_by_id("next",1,0)
                if time == 3:
                    return False

            fun = lambda:search_view_by_id("next")
            wait_for_fun(fun,True,10)

            click_button_by_id("next",1,0)
            sleep(3)

            click_textview_by_id("account_name",1,0)
            clear_edittext_by_id("account_name",1,0)
            sleep(1)
            ime.IME_input_english(1,"autotest")
            #entertext_edittext_by_id("account_name",SC.PRIVATE_EMAIL_ACCOUNT_NAME,1,0)

            click_button_by_id("next",1,0)
            sleep(1)
            goback()
            goback()
            return True
        else:
            goback()
            goback()
            goback()
            goback()
            goback()
            return False

    #write an email ,only text
    def write_email(self, to_address, subject, content):

        ime = IME()

        #input to_address
        clear_edittext_by_id("to",1,0)
        ime.IME_input(1,to_address)

        #input subject
        click_textview_by_id("subject")
        ime.IME_input(1,subject)

        #input content
        ime.IME_input(1,content)
        #entertext_edittext_by_id("body_text",content)
        click_imageview_by_id("send")
