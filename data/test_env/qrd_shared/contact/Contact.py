from case_utility import *
from qrd_shared.Base import Base
from qrd_shared.case import *
import settings.common as SC

class Contact(Base):
    def __init__(self):
        """
        This function init share contact api class.
        @return: none
        """

        self.mode_name = "contact"
        self.tag = 'qrd_share_contact'
        Base.__init__(self, self.mode_name)
        self.debug_print('contact init:%f' % (time.time()))

    def add_contact_to_sim_card(self, i):
        """
        This function share api for others add contact to simcard.
        @type  name: string
        @param name: name
        @type  number: number
        @param number: phone number

        @return: none
        """

        click_imageview_by_id('menu_add_contact')
        click_textview_by_id('account_type')
        click_textview_by_text('SIM Card')

        entertext_edittext_by_index("0",'test' + str(i+1))
        entertext_edittext_by_index("1",'10086')

        #click btn done
        click_imageview_by_id('icon')
        return
    
    def add_contact_to_phone(self, i):
        """
        This function share api for others add contact to phone.
        @type  name: string
        @param name: name
        @type  number: number
        @param number: phone number

        @return: none
        """

        click_imageview_by_id('menu_add_contact')
        click_textview_by_id('account_type')
        click_textview_by_text('PHONE')

        entertext_edittext_by_index("0",'test' + str(i+1))
        entertext_edittext_by_index("2",'10086')

        #click btn done
        click_imageview_by_id('icon')
        return
    
    def del_contact_all(self):
        """
        This function del all contact records
        @return:  none
        """
        if search_text("test"):
            send_key(KEY_MENU)
            delstr = self.get_value('contact_delete')
            if search_text(delstr):
                click_textview_by_text(delstr)
                click_checkbox_by_id('select_all_check')
                click_button_by_text(self.get_value('ok'))
                click_button_by_text(self.get_value('ok'))
                if wait_for_fun(lambda:search_text(self.get_value("set_up_my_profile")), True, 10):
                    return
            else:
                return
        else:
            return

    def del_contact(self, i):
        """
        This function del one contact record
        @return:  none
        """
        if search_text('test' + str(i+1)):
            click_textview_by_text('test' + str(i+1))
            send_key(KEY_MENU)
            click_textview_by_text(self.get_value('contact_delete'))
            click_button_by_text(self.get_value('ok'))
            return
        else:
            return
