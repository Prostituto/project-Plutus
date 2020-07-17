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


class Logic():
    def __init__(self):
        # Initialize the IQ Option API
        self.Plutus = IQ_Option(test_accounts["email_1"], test_accounts["password_1"])

        # Utility Variables -----------------------------------------------------------------------------------------------------------
        self.iq_option_api_version = self.get_iq_option_api_version()
        self.server_timestamp = 0

        # Connection Status
        self.is_connected = False
        self.connection_status_reason = ""

        # Default User-Agent is "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
        self.header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:70.0 Gecko/20100101 Firefox/70.0"}
        self.cookie = {"Plutus": "GOOD"}

        # For Authentication
        self.error_password = "{"\
            "\"code\":\"invalid_credentials\","\
            "\"message\":\"You entered the wrong credentials. Please check that the login/password is correct.\""\
        "}"
        # End of: Utility Variables ---------------------------------------------------------------------------------------------------

        self.Plutus.set_session(self.header, self.cookie)

        response = self.connect_to_server()
        self.is_connected = response["is_connected"]
        self.connection_status_reason = response["connection_status_reason"]

        if self.is_connected:
            print("######### [ Success ] >> First Connection Attempt to the iq option Server #########")

            self.server_timestamp = self.get_server_timestamp()

            # Global Variables --------------------------------------------------------------------------------------------------------
            # All User Information Plus Balances and Others
            self.acct_data = self.get_acct_data_online()

            # User Information
            self.id = self.acct_data["id"]
            self.name = self.acct_data["name"]
            self.nickname = self.acct_data["nickname"]
            self.gender = self.acct_data["gender"]
            self.birthdate = self.acct_data["birthdate"]
            self.nationality = self.acct_data["nationality"]
            self.address = self.acct_data["address"]
            self.email = self.acct_data["email"]
            self.phone = self.acct_data["phone"]
            
            # Other/All Account Balances Data
            self.balances = self.acct_data["balances"]
            self.real_balance = self.balances[0]
            self.practice_balance = self.balances[1]

            # Current Account Balance Data
            self.balance = self.acct_data["balance"]
            self.balance_id = self.acct_data["balance_id"]
            self.balance_type = self.acct_data["balance_type"]
            self.currency = self.acct_data["currency"]
            self.currency_char = self.acct_data["currency_char"]
            # End of: Global Variables ------------------------------------------------------------------------------------------------
        else:
            print("######### [ FAIL ] >> First Connection Attempt to the iq option Server #########")
            print("######### [ REASON ] >>", self.connection_status_reason, "#########")
    
    # Utility Functions
    def get_iq_option_api_version(self):
        return IQ_Option.__version__

    def connect_to_server(self):
        is_connected, connection_status_reason =  self.Plutus.connect()

        return {
            "is_connected": is_connected,
            "connection_status_reason": connection_status_reason
        }

    def check_connection(self):
        return self.Plutus.check_connect()

    def get_server_timestamp(self):
        return self.Plutus.get_server_timestamp()

    # Getter Functions
    def get_acct_data_online(self):
        return self.Plutus.get_profile_ansyc()

    def get_balances_data_online(self):
        return self.Plutus.get_balances()

    def get_real_balance_data(self, balances):
        return balances[0]

    def get_practice_balance_data(self, balances):
        return balances[1]

    # Setter Functions


class Bridge():
    def __init__(self):
        gui = GUI()
        logic = Logic()

        self.initialize_gui_values()

    def initialize_gui_values(self):
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
        grid_account_info = QGridLayout()
        grid_account_info.setSpacing(10)

        # Account Balance
        label_balance = QLabel("Balance:")
        grid_account_info.addWidget(label_balance, 0, 0)

        self.label_balance_value = QLabel()
        grid_account_info.addWidget(self.label_balance_value, 0, 1)

        # Currency Type
        label_currency_type = QLabel("Currency Type:")
        grid_account_info.addWidget(label_currency_type, 1, 0)

        self.label_currency_type_value = QLabel(self)
        grid_account_info.addWidget(self.label_currency_type_value, 1, 1)
        
        # Reset Balance Button
        button_reset_balance = QPushButton("Reset Balance")
        # button_reset_balance.clicked.connect(self.reset_balance)

        # Refresh Button
        button_refresh = QPushButton("Refresh")
        # button_refresh.clicked.connect(self.refresh_everything)

        # Group Box - Account Informaiton
        group_box_account_info = QGroupBox("Account Information")
        group_box_account_info.setCheckable(False)

        group_box_account_info.setLayout(grid_account_info)

        # Grid Layout - Main
        grid_main = QGridLayout()
        grid_main.setSpacing(10)
        grid_main.addWidget(group_box_account_info, 0, 0)

        self.setLayout(grid_main)
        self.setGeometry(300, 300, 200, 200)
        self.setWindowTitle("Project Plutus - Main Window")
        self.show()
        # =============================================================================================================================
        # End of: Python GUI Setup Using PyQt5
        # =============================================================================================================================

    # Mutator Functions ---------------------------------------------------------------------------------------------------------------
    def set_balance_gui(self, balance):
        self.label_balance_value.setText(str(balance))
        self.label_balance_value.adjustSize()

        return True

    def set_currency_type_gui(self, currency_type):
        self.label_currency_type_value.setText(currency_type)
        self.label_currency_type_value.adjustSize()

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

    Plutus = Logic()

    # Pyhton GUI Initialization
    app = QApplication(sys.argv)
    gui = GUI()

    sys.exit(app.exec_())


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
