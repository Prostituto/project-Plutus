import sys
import time
# import json
import logging    # Debug mode on

from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout,
    QGroupBox, QPushButton, QLabel, QLineEdit, QMessageBox)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

from iqoptionapi.stable_api import IQ_Option
from accounts import test_accounts


class API():
    def __init__(self):
        # Initialize the IQ Option API
        self.__Plutus = IQ_Option(test_accounts["email_1"], test_accounts["password_1"])

        # Utility Variables -----------------------------------------------------------------------------------------------------------        
        self.__iq_option_api_version = IQ_Option.__version__
        self.__server_timestamp = 0

        # Connection Status
        self.__is_connected = False
        self.__connection_status_reason = ""

        # Default User-Agent is "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
        self.__header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:70.0 Gecko/20100101 Firefox/70.0"}
        self.__cookie = {"Plutus": "GOOD"}

        # For Authentication
        self.__error_password = "{"\
            "\"code\":\"invalid_credentials\","\
            "\"message\":\"You entered the wrong credentials. Please check that the login/password is correct.\""\
        "}"
        # End of: Utility Variables ---------------------------------------------------------------------------------------------------

        self.__Plutus.set_session(self.__header, self.__cookie)

        server_response = self.connect_to_server()
        self.set_is_connected(server_response)
        self.set_connection_status_reason(server_response)
        

        if self.get_is_connected():
            print("######### [ Success ] >> First Connection Attempt to the iq option Server #########")

            self.set_server_timestamp_online()

            # Global Variables --------------------------------------------------------------------------------------------------------
            # All User Information Plus Balances and Other Data
            self.__acct_data = self.__Plutus.get_profile_ansyc()

            # User Information Data
            self.__id = self.__acct_data["id"]
            self.__name = self.__acct_data["name"]
            self.__nickname = self.__acct_data["nickname"]
            self.__gender = self.__acct_data["gender"]
            self.__birthdate = self.__acct_data["birthdate"]
            self.__nationality = self.__acct_data["nationality"]
            self.__address = self.__acct_data["address"]
            self.__email = self.__acct_data["email"]
            self.__phone = self.__acct_data["phone"]
            
            # All the Different Balance Type Data
            self.__balances_data = self.__acct_data["balances"]
            self.__real_balance_data = self.__balances_data[0]
            self.__practice_balance_data = self.__balances_data[1]

            # Current Basic Balance Type Data
            self.__current_balance = self.__acct_data["balance"]
            self.__current_balance_id = self.__acct_data["balance_id"]
            self.__current_balance_type = self.__acct_data["balance_type"]
            self.__current_currency = self.__acct_data["currency"]
            self.__current_currency_char = self.__acct_data["currency_char"]
            # End of: Global Variables ------------------------------------------------------------------------------------------------
        else:
            print("######### [ FAIL ] >> First Connection Attempt to the iq option Server #########")
            print("######### [ REASON ] >>", self.__connection_status_reason, "#########")
    
    # Utility Functions ---------------------------------------------------------------------------------------------------------------
    def connect_to_server(self):
        is_connected, connection_status_reason =  self.__Plutus.connect()

        return {
            "is_connected": is_connected,
            "connection_status_reason": connection_status_reason
        }

    def check_connection(self):
        return self.__Plutus.check_connect()
    # End of: Utility Functions -------------------------------------------------------------------------------------------------------

    # Getter Functions ----------------------------------------------------------------------------------------------------------------
    # Get the Utility Variables
    def get_plutus(self):
        return self.__Plutus
    
    def get_iq_option_api_version(self):
        return self.__iq_option_api_version

    def get_server_timestamp(self):
        return self.__server_timestamp
    
    def get_is_connected(self):
        return self.__is_connected

    def get_connection_status_reason(self):
        return self.__connection_status_reason

    def get_header(self):
        return self.__header
    
    def get_cookie(self):
        return self__cookie

    def get_error_password(self):
        self.__error_password

    # Get All of the User Infotmation Plus Balances and Other Data
    def get_acct_data(self):
        return self.__acct_data

    # Get User Information Data
    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_nickname(self):
        return self.__nickname

    def get_gender(self):
        return self.__gender

    def get_birthdate(self):
        return self.__birthdate

    def get_nationality(self):
        return self.__nationality

    def get_address(self):
        return self.__address

    def get_email(self):
        return self.__email

    def get_phone(self):
        return self.__phone
    
    # Get All the Different Balance Type Data
    def get_balances_data(self):
        return self.__balances

    def get_real_balance_data(self, balances):
        return balances[0]

    def get_practice_balance_data(self, balances):
        return balances[1]

    # Get the Current Basic Balance Type Data
    def get_current_balance(self):
        return self.__current_balance

    def get_current_balance_id(self):
        return self.__current_balance_id

    def get_current_balance_type(self):
        return self.__current_balance_type

    def ger_current_currency(self):
        return self.__current_currency

    def get_current_currency_char(self):
        return self.__current_currency_char
    # End of: Getter Functions --------------------------------------------------------------------------------------------------------

    # Setter Functions ----------------------------------------------------------------------------------------------------------------
    # Set the Utility Variables
    def set_iq_option_api(self, email, password):
        self.__Plutus = IQ_Option(email, password)

    def set_iq_option_api_version(self):
        self.__iq_option_api_version = IQ_Option.__version__

    def set_server_timestamp_online(self):
        try:
            self.__server_timestamp = self.__Plutus.get_server_timestamp()
        except:
            print("######### [ ERROR ] >> Cannot Retrieve Server Timestamp #########")

            self.__server_timestamp = 0

    def set_is_connected(self, server_response):
        self.__is_connected = server_response["is_connected"]
    
    def set_connection_status_reason(self, server_response):

        self.__connection_status_reason = server_response["is_connected"]

    def set_header(self, new_header):
        self.__header = new_header

    def set_cookie(self, new_cookie):
        self.__cookie = new_cookie

    def set_error_password(self, new_error_password):
        self.__error_password = new_error_password

    # Set All of the User Information Plus Balances and Other Data
    def set_acct_data_online(self):
        self.__acct_data = self.__Plutus.get_profile_ansyc()

    # Set User Information Data
    def set_id(self, acct_data):
        self.__id = acct_data["id"]
    
    def set_name(self, acct_data):
        self.__name = acct_data["name"]

    def set_nickname(self, acct_data):
        self.__nickname = acct_data["nickname"]

    def set_gender(self, acct_data):
        self.__gender = acct_data["gender"]
    
    def set_birthdate(self, acct_data):
        self.__birthdate = acct_data["birthdate"]

    def set_nationality(self, acct_data):
        self.__nationality = acct_data["nationality"]

    def set_address(self, acct_data):
        self.__address = acct_data["address"]

    def set_email(self, acct_data):
        self.__email = acct_data["email"]
    
    def set_phone(self, acct_data):
        self.__phone = acct_data["phone"]

    # Set All the Different Balance Type Data
    def set_balances_data_online(self):
        self.__balances_data = self.__Plutus.get_profile_ansyc()

    def set_real_balance_data(self, balances_data):
        self.__real_balance_data = balances_data[0]

    def set_practice_balance_data(self, balances_data):
        self.__practice_balance_data = balances_data[1]

    # Set the Current Basic Balance Type Data
    def set_current_balance(self, acct_data):
        self.__current_balance = acct_data["balance"]

    def set_current_balance_id(self, acct_data):
        self.__current_balance_id = acct_data["balance_id"]
    
    def set_current_balance_type(self, acct_data):
        self.__current_balance_type = acct_data["balance_type"]
        
    def set_current_currency_char(self, acct_data):
        self.__current_currency_char = acct_data["currency_char"]
    # End of: Setter Functions ----------------------------------------------------------------------------------------------------------------


class Logic():
    def __init__(self):
        app = QApplication(sys.argv)
        self.gui = GUI()

        self.api = API()

        self.initialize_gui_values()

        sys.exit(app.exec_())

    def initialize_gui_values(self):
        self.gui.set_current_balance(self.api.get_current_balance())
        self.gui.set_current_currency_type(self.api.get_current_currency_char())
        pass


class GUI(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initialize_gui()

        # Global Variables ------------------------------------------------------------------------------------------------------------
        # End of: Global Variables ----------------------------------------------------------------------------------------------------

        # Utility Variables -----------------------------------------------------------------------------------------------------------
        # End of: Utility Variables ---------------------------------------------------------------------------------------------------

    def initialize_gui(self):
        # =============================================================================================================================
        # Python GUI Setup Using PyQt5
        # =============================================================================================================================
        __grid_acct_info = QGridLayout()
        __grid_acct_info.setSpacing(10)

        # Account Balance
        __lbl_current_balance = QLabel("Balance:")
        __grid_acct_info.addWidget(__lbl_current_balance, 0, 0)

        self.__lbl_current_balance_value = QLabel()
        __grid_acct_info.addWidget(self.__lbl_current_balance_value, 0, 1)

        # Currency Type
        __lbl_current_currency_type = QLabel("Currency Type:")
        __grid_acct_info.addWidget(__lbl_current_currency_type, 1, 0)

        self.__lbl_current_currency_type_value = QLabel(self)
        __grid_acct_info.addWidget(self.__lbl_current_currency_type_value, 1, 1)
        
        # Reset Balance Button
        __btn_reset_balance = QPushButton("Reset Balance")
        # button_reset_balance.clicked.connect(self.reset_balance)

        # Refresh Button
        __btn_refresh = QPushButton("Refresh")
        # button_refresh.clicked.connect(self.refresh_everything)

        # Group Box - Account Informaiton
        __group_box_acct_info = QGroupBox("Account Information")
        __group_box_acct_info.setCheckable(False)

        __group_box_acct_info.setLayout(__grid_acct_info)

        # Grid Layout - Main
        __grid_main = QGridLayout()
        __grid_main.setSpacing(10)
        __grid_main.addWidget(__group_box_acct_info, 0, 0)

        self.setLayout(__grid_main)
        self.setGeometry(300, 300, 200, 200)
        self.setWindowTitle("Project Plutus - Main Window")
        self.show()
        # =============================================================================================================================
        # End of: Python GUI Setup Using PyQt5
        # =============================================================================================================================

    # Mutator Functions ---------------------------------------------------------------------------------------------------------------
    def set_current_balance(self, current_balance):
        self.__lbl_current_balance_value.setText(str(current_balance))
        self.__lbl_current_balance_value.adjustSize()

        return True

    def set_current_currency_type(self, current_currency_type):
        self.__lbl_current_currency_type_value.setText(current_currency_type)
        self.__lbl_current_currency_type_value.adjustSize()

        return True
    # End of: Mutator Funcions --------------------------------------------------------------------------------------------------------

    # Accessor Functions --------------------------------------------------------------------------------------------------------------
    # End of: Accessor Functions ------------------------------------------------------------------------------------------------------

    # Utility Functions ---------------------------------------------------------------------------------------------------------------
    # End of: Utility Functions -------------------------------------------------------------------------------------------------------


def main():
    current_local_time = str(time.ctime()).replace(":", "-")
    log_file_name = current_local_time + " iq_option_connection"

    """
    # Debug mode on
    logging.basicConfig(filename="logs/" + log_file_name + ".log",
                        format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
                        # datefmt="%H:%M:%S",
                        level=logging.DEBUG)
    """

    # Debug mode on
    logging.basicConfig(format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
                        # datefmt="%H:%M:%S",
                        level=logging.DEBUG)

    # Pyhton GUI Initialization
    logic = Logic()


if __name__ == "__main__":
    main()
    

"""
# =========================================================================================================================
# Check connection and attemp to reconnect if ever needed. 
# =========================================================================================================================
if check:
    print("######### Starting Your Robot #########")    # If you can see this, then you can close network for test.

    while True:
        if Plutus.check_connect() == False:    # Detect if the websocket is close.
            print("######### Trying to Reconnect #########")
            check, reason = Plutus.connect()    # Connect to iq option again.

            if check:
                print("######### Reconnected Successfully #########")
            else:
                if reason == error_password:
                    print("######### Password Error #########")
                else:
                    print("######### Network Error #########")
else:
    if reason == "[Errno -2] Name or service not known":
        print("######### Network Error #########")
    elif reason == error_password:
        print("######### Password Error #########")
    else:
        print("######### Just Error #########")
# =========================================================================================================================
# End of: Check connection and attemp to reconnect if ever needed.
# =========================================================================================================================
"""

# =========================================================================================================================
# Account
# =========================================================================================================================
# Plutus.get_balance_v2()    # Not working.
# print("######### Balance v2 #########", balance_v2, "######### Balance v2 #########")
# =========================================================================================================================
# End of: Account
# =========================================================================================================================

"""
goal = "EURUSD"
print("get candles")
print(Plutus.get_candles(goal, 60, 111, time.time()))
"""
