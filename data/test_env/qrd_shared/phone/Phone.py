from case_utility import *
from qrd_shared.Base import Base
import settings.common as SC
from qrd_shared.language.language import Language
from qrd_shared.settings.Settings import Settings
import time

PREDEFINED_NUMBERS = {"0": "zero", "1": "one", "2": "two", "3": "three", "4": "four", "5": "five", "6": "six", "7": "seven", "8": "eight", "9": "nine"}
CALL_DELAY = 0
CALL_INI_TIME = 0
CALL_START_TIME = 0

class Phone(Base):
     
    def __init__(self):
        self.mode_name = "phone"
        Base.__init__(self,self.mode_name)
        self.settings = Settings()
        self.predefined_numbers = PREDEFINED_NUMBERS
        self.debug_print( 'Base init:%f' %(time.time()))
        self.call_delay = CALL_DELAY
        self.call_ini_time = CALL_INI_TIME
        self.call_start_time = CALL_START_TIME  
       

    def phone_call(self, call_number, slot, call_duration):
        
        numberlist = self.predefined_numbers

        drag_by_param(0,50,100,50,10)
        drag_by_param(0,50,100,50,10)
        #clear existing number
        click_imageview_by_id("deleteButton",clickType=LONG_CLICK)

        call_number_str = [s for s in call_number ]
            
        for callnumber in call_number_str:
            click_imageview_by_id(numberlist[callnumber])
        
        click_imageview_by_id("dialButton")
        self.call_ini_time=time.strftime('%X',time.localtime(time.time()))
        
#        if SC.PUBLIC_DSDS:
#            callmark = ""
#            if slot == 0:
#                callmark = "callmark1"
#            elif slot == 1:
#                callmark = "callmark2"
#            click_button_by_id(callmark)

        #MO
        phoneOn = self.check_phoneON(10)
        
        if phoneOn:
            sleep(call_duration)
            if search_view_by_id("endButton"):
                click_button_by_id("endButton")
                return True
            else:
                return False
#    def call_delay(self):
        
    def phone_call_from_list(self, slot):

        drag_by_param(0,50,100,50,10)
        drag_by_param(0,50,100,50,10)
        drag_by_param(90,50,10,50,10)

        #Choose a number
        click_textview_by_text('10086' or 'test')
        
        #Dial
        click_textview_by_text('Call')
        
        #Choose a slot
        if SC.PUBLIC_DSDS:
            callmark = ""
            if slot == 0:
                callmark = "callmark1"
            elif slot == 1:
                callmark = "callmark2"
            click_button_by_id(callmark)
        
        #MO
        phoneOn = self.check_phoneON(10)
    
        if phoneOn:
            time.sleep(1)
            if search_view_by_id("endButton"):
                click_button_by_id("endButton")
                return True
            else:
                return False

    def phone_call_multiparty(self,call_number1,call_number2,call_slot,call_duration):
        
        numberlist = self.predefined_numbers
        drag_by_param(0,50,100,50,10)
        drag_by_param(0,50,100,50,10)
        
        #clear existing number
        click_imageview_by_id("deleteButton",clickType=LONG_CLICK)

        call_number_str = [s for s in call_number1]
        for callnumber in call_number_str:
            click_imageview_by_id(numberlist[callnumber])
        click_imageview_by_id("dialButton")
        if SC.PUBLIC_DSDS:
            callmark = ""
            if call_slot == 0:
                callmark = "callmark1"
            elif call_slot == 1:
                callmark = "callmark2"
            click_button_by_id(callmark)
        sleep(5)
        click_imageview_by_id("addButton")
#        click_imageview_by_index(3)
        call_number_str = [s for s in call_number2]
        for callnumber in call_number_str:
            click_imageview_by_id(numberlist[callnumber])
        click_imageview_by_id("dialButton")
        sleep(5)
        click_imageview_by_id("mergeButton")
            
        phoneOn = False
        phoneOn = self.check_phoneON(30)

        if phoneOn:
            sleep(call_duration)
            if search_view_by_id("endButton"):
                click_button_by_id("endButton")
                return True
            else:
                return False
                save_fail_log()

    def check_phoneON(self, starttime):

#        if search_text(self.get_value("network_not_available")):
#            return False
        if search_view_by_id("message"):
            return False
        #whether get through.
        phoneOn = False
        t = 0
        while search_view_by_id("endButton") and t < starttime:
            if search_text("0:"):
                self.call_start_time=time.strftime('%X',time.localtime(time.time()))
                phoneOn = True
                sleep(3)
                break
            sleep(1)
            t = t+1
        time_start_strlis=self.call_ini_time.split(':')
        time_end_strlis=self.call_start_time.split(':')
        sec=int(time_end_strlis[2])+int(time_end_strlis[1])*60+int(time_end_strlis[0])*60*60-int(time_start_strlis[2])-int(time_start_strlis[1])*60-int(time_start_strlis[0])*60*60
        self.call_delay = sec
        if phoneOn == False:
            return False
        else:
            return True

    #remove guide info when enter phone app for the first time
    def remove_gudie_info(self):
        
        if search_view_by_id("clingText") == True:
            click_button_by_text(self.get_value("ok"),1,0)

    #data call switch to always ask
    #parameter:
    #    card_id,1-slot1,2-slot2,0-always ask
    
    def set_data_call(self, card_id):
        
        sleep(1)
        #remove guide info when enter first time
        self.remove_gudie_info()

        start_activity('com.android.settings','.Settings')
        self.settings.set_default_voice(card_id)
        goback()

    #used for API
    def smart_dial(self, smartNumber, phoneNumber):
        
        click_imageview_by_id("deleteButton",1,0,0,LONG_CLICK)
        for i in range(0, len(smartNumber)):
            click_imageview_by_id(str(PREDEFINED_NUMBERS[smartNumber[i]]))
        click_view_by_container_id('filterbutton', 'android.widget.TextView', 0)
        sleep(1)
        click_textview_by_text(phoneNumber)
        click_imageview_by_id("dialButton")
    
    def dial(self, call_number, slot, call_duration):
        
        numberlist = self.predefined_numbers

        drag_by_param(0,50,100,50,10)
        drag_by_param(0,50,100,50,10)

        #clear existing number
        click_imageview_by_id("deleteButton",clickType=LONG_CLICK)

        call_number_str = [s for s in call_number ]
            
        for callnumber in call_number_str:
            click_imageview_by_id(numberlist[callnumber])
        
        click_imageview_by_id("dialButton")
        
        #MO
        phoneOn = False
        phoneOn = self.check_phoneON(30)
        return phoneOn

    def call_waiting_on(self,slot):
        if SC.PUBLIC_DSDS:
            click_textview_by_text(self.get_value("select_subscription"))
            if slot == 0:
                click_textview_by_text(self.get_value("sim1"))
            else:
                click_textview_by_text(self.get_value("sim2"))
            click_textview_by_text(self.get_value("GSM_call_settings"))
            click_textview_by_text(self.get_value("additional_settings"))
            sleep(15)
            flag = is_checkbox_checked_by_index(0)
            if flag == False:
                click_textview_by_text(self.get_value("call_waiting"))
                sleep(15)
        else:
            click_textview_by_text(self.get_value("additional_settings"))
            sleep(15)
            flag = is_checkbox_checked_by_index(0)
            if flag == False:
                click_textview_by_text(self.get_value("call_waiting"))
                sleep(15)
            
            
            
    def call_waiting_off(self,slot):
        if SC.PUBLIC_DSDS:
            click_textview_by_text(self.get_value("select_subscription"))
            if slot == 0:
                click_textview_by_text(self.get_value("sim1"))
            else:
                click_textview_by_text(self.get_value("sim2"))
            click_textview_by_text(self.get_value("GSM_call_settings"))
            click_textview_by_text(self.get_value("additional_settings"))
            sleep(15)
            flag = is_checkbox_checked_by_index(0)
            if flag == True:
                click_textview_by_text(self.get_value("call_waiting"))
                sleep(15)
        else:
            click_textview_by_text(self.get_value("additional_settings"))
            sleep(15)
            flag = is_checkbox_checked_by_index(0)
            if flag == True:
                click_textview_by_text(self.get_value("call_waiting"))
                sleep(15)

    def call_forwarding_on(self,forward_num,type,slot):
        if SC.PUBLIC_DSDS:
            click_textview_by_text(self.get_value("select_subscription"))
            if slot == 0:
                click_textview_by_text(self.get_value("sim1"))
            else:
                click_textview_by_text(self.get_value("sim2"))
            click_textview_by_text(self.get_value("GSM_call_settings"))
            click_textview_by_text(self.get_value("call_forwarding"))
            sleep(15)
            '''
            type 0: always forward
            type 1-3: other forward type
            '''
            if type == 0:
                if not search_text(self.get_value("forward_all_calls_status"),0,0):
                    click_textview_by_text(self.get_value("always_forward"))
                    entertext_edittext_by_id('edit',forward_num)
                    click_button_by_id('button3')
                    sleep(15)
            elif type == 1:
                if not search_text(self.get_value("forward_other_status"),0,0):
                    click_textview_by_text(self.get_value("forward_when_busy"))
                    entertext_edittext_by_id('edit',forward_num)
                    click_button_by_id('button3')
                    sleep(15)
            elif type ==2:
                if not search_text(self.get_value("forward_other_status"),0,0):
                    click_textview_by_text(self.get_value("forward_when_unanswered"))
                    entertext_edittext_by_id('edit',forward_num)
                    click_button_by_id('button3')
                    sleep(15)
            elif type ==3:
                if not search_text(self.get_value("forward_other_status"),0,0):
                    click_textview_by_text(self.get_value("forward_when_unreachable"))
                    entertext_edittext_by_id('edit',forward_num)
                    click_button_by_id('button3')
                    sleep(15)
        else:
            click_textview_by_text(self.get_value("call_forwarding"))
            sleep(15)
            '''
            type 0: always forward
            type 1-3: other forward type
            '''
            if type == 0:
                if not search_text(self.get_value("forward_all_calls_status"),0,0):
                    click_textview_by_text(self.get_value("always_forward"))
                    entertext_edittext_by_id('edit',forward_num)
                    click_button_by_id('button3')
                    sleep(15)
            elif type == 1:
                if not search_text(self.get_value("forward_other_status"),0,0):
                    click_textview_by_text(self.get_value("forward_when_busy"))
                    entertext_edittext_by_id('edit',forward_num)
                    click_button_by_id('button3')
                    sleep(15)
            elif type ==2:
                if not search_text(self.get_value("forward_other_status"),0,0):
                    click_textview_by_text(self.get_value("forward_when_unanswered"))
                    entertext_edittext_by_id('edit',forward_num)
                    click_button_by_id('button3')
                    sleep(15)
            elif type ==3:
                if not search_text(self.get_value("forward_other_status"),0,0):
                    click_textview_by_text(self.get_value("forward_when_unreachable"))
                    entertext_edittext_by_id('edit',forward_num)
                    click_button_by_id('button3')
                    sleep(15)
                
    def call_forwarding_off(self,type,slot):
        if SC.PUBLIC_DSDS:
            click_textview_by_text(self.get_value("select_subscription"))
            if slot == 0:
                click_textview_by_text(self.get_value("sim1"))
            else:
                click_textview_by_text(self.get_value("sim2"))
            click_textview_by_text(self.get_value("GSM_call_settings"))
            click_textview_by_text(self.get_value("call_forwarding"))
            sleep(15)
            '''
            type 0: always forward
            '''
            if type == 0:
                if search_text(self.get_value("forward_all_calls_status"),0,0):
                    click_textview_by_text(self.get_value("always_forward"))
                    click_button_by_id('button3')
                    sleep(15)
            elif type == 1:
                if search_text(self.get_value("forward_other_status"),0,0):
                    click_textview_by_text(self.get_value("forward_when_busy"))
                    click_button_by_id('button3')
                    sleep(15)
            elif type ==2:
                if search_text(self.get_value("forward_other_status"),0,0):
                    click_textview_by_text(self.get_value("forward_when_unanswered"))
                    click_button_by_id('button3')
                    sleep(15)
            elif type ==3:
                if search_text(self.get_value("forward_other_status"),0,0):
                    click_textview_by_text(self.get_value("forward_when_unreachable"))
                    click_button_by_id('button3')
                    sleep(15)
        else:
            click_textview_by_text(self.get_value("call_forwarding"))
            sleep(15)
            '''
            type 0: always forward
            '''
            if type == 0:
                if search_text(self.get_value("forward_all_calls_status"),0,0):
                    click_textview_by_text(self.get_value("always_forward"))
                    click_button_by_id('button3')
                    sleep(15)
            elif type == 1:
                if search_text(self.get_value("forward_other_status"),0,0):
                    click_textview_by_text(self.get_value("forward_when_busy"))
                    click_button_by_id('button3')
                    sleep(15)
            elif type ==2:
                if search_text(self.get_value("forward_other_status"),0,0):
                    click_textview_by_text(self.get_value("forward_when_unanswered"))
                    click_button_by_id('button3')
                    sleep(15)
            elif type ==3:
                if search_text(self.get_value("forward_other_status"),0,0):
                    click_textview_by_text(self.get_value("forward_when_unreachable"))
                    click_button_by_id('button3')
                    sleep(15)   
    def mtcall(self,call_number_slot1,call_repeat_times_slot1,call_duration,waittime,intervaltime):
        
        click_textview_by_text("MT Call")
        click_textview_by_text("Add")
        entertext_edittext_by_index(0,call_number_slot1)
        click_textview_by_text("Ok")
        entertext_edittext_by_index(1,call_repeat_times_slot1)
        entertext_edittext_by_index(2,call_duration)
        entertext_edittext_by_index(3,waittime)
        entertext_edittext_by_index(4,intervaltime)
        goback()
        click_textview_by_text("Send")
        sleep(15)
        
    def check_call_status(self):
        
        if search_text(self.get_value("return")):
        #click_button_by_text("Return to call in progress")
            click_textview_by_text(self.get_value("return"))
            if search_view_by_id("endButton"):
                click_button_by_id("endButton")
                return True
            else:
                return False
        else:
            return False
        
    def clear_call_log(self):
        
        drag_by_param(0,50,100,50,10)
        drag_by_param(0,50,100,50,10)
        drag_by_param(90,50,10,50,10)
        
        if not search_text(self.get_value("call_log_is_empty")):
            send_key(KEY_MENU)
            clear_call_log = self.get_value("clear_call_log")
            if wait_for_fun(lambda:search_text(clear_call_log), True, 3):
                click_textview_by_text(clear_call_log)
                click_checkbox_by_id('select_all_check')
                click_button_by_text(self.get_value('ok'))
                click_button_by_text(self.get_value('ok'))
                wait_for_fun(lambda:search_text(self.get_value("call_log_is_empty")), True, 10)
                return
            else:
                return
        else:
            return
    def call_autoanswer_enable(self):
        if not is_checkbox_checked_by_index(0):
            click_checkbox_by_id("checkbox")
        
    def call_autoanswer_disable(self):
        if is_checkbox_checked_by_index(0):
            click_checkbox_by_id("checkbox")

