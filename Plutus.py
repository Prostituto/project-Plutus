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

        # Utility Variables -------------------------------------------------------------------------------------------------------------------
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
        # End of: Utility Variables -----------------------------------------------------------------------------------------------------------

        self.__Plutus.set_session(self.__header, self.__cookie)

        server_response = self.connect_to_server()
        self.set_is_connected(server_response)
        self.set_connection_status_reason(server_response)
        

        if self.get_is_connected():
            print("######### [ Success ] >> First Connection Attempt to the iq option Server #########")

            self.set_server_timestamp_online()

            # Global Variables ----------------------------------------------------------------------------------------------------------------
            # All User Information Plus Balances and Other Data
            self.__acct_data = self.__Plutus.get_profile_ansyc()

            # User Information Data
            self.__user_id = self.__acct_data["user_id"]
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
            self.__balance = self.__acct_data["balance"]
            self.__balance_id = self.__acct_data["balance_id"]
            self.__balance_type = self.__acct_data["balance_type"]
            self.__currency = self.__acct_data["currency"]
            self.__currency_char = self.__acct_data["currency_char"]
            # End of: Global Variables --------------------------------------------------------------------------------------------------------
        else:
            print("######### [ FAIL ] >> First Connection Attempt to the iq option Server #########")
            print("######### [ REASON ] >>", self.__connection_status_reason, "#########")
    
    # Utility Functions -----------------------------------------------------------------------------------------------------------------------
    def connect_to_server(self):
        is_connected, connection_status_reason =  self.__Plutus.connect()

        return {
            "is_connected": is_connected,
            "connection_status_reason": connection_status_reason
        }

    def check_connection(self):
        return self.__Plutus.check_connect()
    # End of: Utility Functions ---------------------------------------------------------------------------------------------------------------

    # Getter Functions ------------------------------------------------------------------------------------------------------------------------
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
        return self.__cookie

    def get_error_password(self):
        self.__error_password

    # Get All of the User Infotmation Plus Balances and Other Data
    def get_acct_data(self):
        return self.__acct_data

    # Get User Information Data
    def get_user_id(self):
        return self.__user_id

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
    def get_balance(self):
        return self.__balance

    def get_balance_id(self):
        return self.__balance_id

    def get_balance_type(self):
        return self.__balance_type

    def ger_currency(self):
        return self.__currency

    def get_currency_char(self):
        return self.__currency_char
    # End of: Getter Functions ----------------------------------------------------------------------------------------------------------------

    # Setter Functions ------------------------------------------------------------------------------------------------------------------------
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
    def set_user_id(self, acct_data):
        self.__user_id = acct_data["user_id"]
    
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
    def set_balance(self, acct_data):
        self.__balance = acct_data["balance"]

    def set_balance_id(self, acct_data):
        self.__balance_id = acct_data["balance_id"]
    
    def set_balance_type(self, acct_data):
        self.__balance_type = acct_data["balance_type"]
        
    def set_currency_char(self, acct_data):
        self.__currency_char = acct_data["currency_char"]
    # End of: Setter Functions ----------------------------------------------------------------------------------------------------------------


class Logic():
    def __init__(self):
        app = QApplication(sys.argv)
        self.gui = GUI()

        self.api = API()

        self.initialize_gui_values()

        sys.exit(app.exec_())

    def initialize_gui_values(self):
        # Initialize Current User Information Data Display ------------------------------------------------------------------------------------
        self.gui.set_user_id(self.api.get_user_id())    # User ID
        self.gui.set_name(self.api.get_name())    # Name
        self.gui.set_nickname(self.api.get_nickname())    # Nickname
        self.gui.set_gender(self.api.get_gender())    # Gender

        # Birthdate
        birthdate = time.ctime(int(self.api.get_birthdate()))
        self.gui.set_birthdate(birthdate) 

        self.gui.set_nationality(self.api.get_nationality())    # Nationality
        self.gui.set_address(self.api.get_address())    # Address
        self.gui.set_email(self.api.get_email())    # Email
        self.gui.set_phone(self.api.get_phone())    # Phone
        # End of: Initialize Current User Information Data Display ----------------------------------------------------------------------------


class GUI(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initialize_gui()

        # Global Variables --------------------------------------------------------------------------------------------------------------------
        # End of: Global Variables ------------------------------------------------------------------------------------------------------------

        # Utility Variables -------------------------------------------------------------------------------------------------------------------
        # End of: Utility Variables -----------------------------------------------------------------------------------------------------------

    def initialize_gui(self):
        # =====================================================================================================================================
        # Python GUI Setup Using PyQt5
        # =====================================================================================================================================
        # Grid Layout - Main
        __grid_main = QGridLayout()
        __grid_main.setSpacing(10)

        # Initialize User Information Widgets -------------------------------------------------------------------------------------------------
        # Grid Layout - User Information 
        __grid_user_info = QGridLayout()
        __grid_user_info.setSpacing(10)

        # Current User/Account ID
        __lbl_user_id = QLabel("User ID:")
        __grid_user_info.addWidget(__lbl_user_id, 0, 0)

        self.__lbl_user_id_value = QLabel()
        __grid_user_info.addWidget(self.__lbl_user_id_value, 0, 1)

        # Current Account Name
        __lbl_name = QLabel("Full Name:")
        __grid_user_info.addWidget(__lbl_name, 1, 0)

        self.__lbl_name_value = QLabel()
        __grid_user_info.addWidget(self.__lbl_name_value, 1, 1)

        # Current Account Nickname
        __lbl_nickname = QLabel("Nickname:")
        __grid_user_info.addWidget(__lbl_nickname, 2, 0)

        self.__lbl_nickname_value = QLabel()
        __grid_user_info.addWidget(self.__lbl_nickname_value, 2, 1)

        # Current Account Gender
        __lbl_gender = QLabel("Gender:")
        __grid_user_info.addWidget(__lbl_gender, 3, 0)

        self.__lbl_gender_value = QLabel()
        __grid_user_info.addWidget(self.__lbl_gender_value, 3, 1)

        # Current Account Birthdate
        __lbl_birthdate = QLabel("Birthdate:")
        __grid_user_info.addWidget(__lbl_birthdate, 4, 0)

        self.__lbl_birthdate_value = QLabel()
        __grid_user_info.addWidget(self.__lbl_birthdate_value, 4, 1)

        # Current Account Nationality
        __lbl_nationality = QLabel("Nationality:")
        __grid_user_info.addWidget(__lbl_nationality, 5, 0)

        self.__lbl_nationality_value = QLabel()
        __grid_user_info.addWidget(self.__lbl_nationality_value, 5, 1)

        # Current Account Address
        __lbl_address = QLabel("Address:")
        __grid_user_info.addWidget(__lbl_address, 6, 0)

        self.__lbl_address_value = QLabel()
        __grid_user_info.addWidget(self.__lbl_address_value, 6, 1)

        # Current Account Email
        __lbl_email = QLabel("Email:")
        __grid_user_info.addWidget(__lbl_email, 7, 0)

        self.__lbl_email_value = QLabel()
        __grid_user_info.addWidget(self.__lbl_email_value, 7, 1)

        # Current Account Phone
        __lbl_phone = QLabel("Phone:")
        __grid_user_info.addWidget(__lbl_phone, 8, 0)

        self.__lbl_phone_value = QLabel()
        __grid_user_info.addWidget(self.__lbl_phone_value, 8, 1)

        # Group Box - Current User Informaiton
        __group_box_user_info = QGroupBox("User Information")
        __group_box_user_info.setCheckable(False)

        __group_box_user_info.setLayout(__grid_user_info)
        
        __grid_main.addWidget(__group_box_user_info, 0, 0)
        # End of: Initialize User Information Widgets -----------------------------------------------------------------------------------------

        self.setLayout(__grid_main)
        self.setGeometry(300, 300, 200, 200)
        self.setWindowTitle("Project Plutus - Main Window")
        self.show()
        # =====================================================================================================================================
        # End of: Python GUI Setup Using PyQt5
        # =====================================================================================================================================

    # Setter Functions ------------------------------------------------------------------------------------------------------------------------
    # Set Current User/Account ID
    def set_user_id(self, user_id):
        self.__lbl_user_id_value.setText(str(user_id))
        self.__lbl_user_id_value.adjustSize()

    # Set Current Account Name
    def set_name(self, name):
        self.__lbl_name_value.setText(str(name))
        self.__lbl_name_value.adjustSize()

    # Set Current Nickname
    def set_nickname(self, nickname):
        self.__lbl_nickname_value.setText(nickname)
        self.__lbl_nickname_value.adjustSize()

    # Set Current Account Gender
    def set_gender(self, gender):
        self.__lbl_gender_value.setText(str(gender))
        self.__lbl_gender_value.adjustSize()

    # Set Current Account Birthdate
    def set_birthdate(self, birthdate):
        self.__lbl_birthdate_value.setText(str(birthdate))
        self.__lbl_birthdate_value.adjustSize()

    # Set Current Account Nationality
    def set_nationality(self, nationality):
        self.__lbl_nationality_value.setText(str(nationality))
        self.__lbl_nationality_value.adjustSize()

    # Set Current Account Address
    def set_address(self, address):
        self.__lbl_address_value.setText(str(address))
        self.__lbl_address_value.adjustSize()

    # Set Current Account Email
    def set_email(self, email):
        self.__lbl_email_value.setText(str(email))
        self.__lbl_email_value.adjustSize()

    # Set Current Account Phone
    def set_phone(self, phone):
        self.__lbl_phone_value.setText(str(phone))
        self.__lbl_phone_value.adjustSize()

    # Set Current Account Type Value
    def set_balance_type(self, balance_type):
        self.__lbl_balance_type_value.setText(str(balance_type))
        self.__lbl_balance_type_value.adjustSize()
    # End of: Setter Funcions -----------------------------------------------------------------------------------------------------------------

    # Accessor Functions ----------------------------------------------------------------------------------------------------------------------
    # End of: Accessor Functions --------------------------------------------------------------------------------------------------------------

    # Utility Functions -----------------------------------------------------------------------------------------------------------------------
    # End of: Utility Functions ---------------------------------------------------------------------------------------------------------------


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
