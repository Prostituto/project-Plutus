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
        # Initialize IQ Option API
        self.Plutus = IQ_Option(test_accounts["email_1"], test_accounts["password_1"])

        # Global Variables --------------------------------------------------------------------------------------------------------
        acct_data = self.get_acct_data_online()
        self.set_global_variables(acct_data)

        self.is_connected = False
        self.connection_status_reason = ""
        # End of: Global Variables ------------------------------------------------------------------------------------------------
    
    # Utility Functions
    def connect_to_server(self):
        self.is_connected, self.connection_status_reason =  self.Plutus.connect()

    # Getter Functions
    def get_balances_online(self):
        pass

    def get_acct_data_online(self):
        return self.Plutus.get_profile_ansyc()

    # Setter Functions
    def set_global_variables(self, acct_data):
        self.id = acct_data["id"]
        self.name = acct_data["name"]
        self.nickname = acct_data["nickname"]
        self.gender = acct_data["gender"]
        self.birthdate = acct_data["birthdate"]
        self.nationality = acct_data["nationality"]
        self.address = acct_data["address"]
        self.email = acct_data["email"]
        self.phone = acct_data["phone"]
        
        self.balances = acct_data["balances"]
        self.balance = acct_data["balance"]
        self.balance_id = acct_data["balance_id"]
        self.balance_type = acct_data["balance_type"]
        self.currency = acct_data["currency"]
        self.currency_char = acct_data["currency_char"]


class Window(QWidget):
    def __init__(self, Plutus, initial_data):
        super().__init__()
        self.initialize_UI()

        # Global Variables --------------------------------------------------------------------------------------------------------
        self.Plutus = Plutus
        self.iq_option_API_version = initial_data["iq_option_API_version"]
        self.is_connected = initial_data["is_connected"]
        self.connection_status_reason = initial_data["connection_status_reason"]
        self.server_timestamp = initial_data["server_timestamp"]

        self.balance = initial_data["balance"]
        self.currency_type = initial_data["currency_type"]
        # End of: Global Variables ------------------------------------------------------------------------------------------------

        # Utility Variables -------------------------------------------------------------------------------------------------------
        self.error_password = "{"\
            "\"code\":\"invalid_credentials\","\
            "\"message\":\"You entered the wrong credentials. Please check that the login/password is correct.\""\
        "}"
        # End of: Utility Variables -----------------------------------------------------------------------------------------------

        # Initialize Values
        self.set_balance_gui(self.balance)
        self.set_currency_type_gui(self.currency_type)

    def initialize_UI(self):
        # =========================================================================================================================
        # Python GUI Setup Using PyQt5
        # =========================================================================================================================
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
        button_reset_balance.clicked.connect(self.reset_balance)

        # Refresh Button
        button_refresh = QPushButton("Refresh")
        button_refresh.clicked.connect(self.refresh_everything)

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
        # =========================================================================================================================
        # End of: Python GUI Setup Using PyQt5
        # =========================================================================================================================

    # Mutator Functions -----------------------------------------------------------------------------------------------------------
    def set_balance_gui(self, balance):
        self.label_balance_value.setText(str(balance))
        self.label_balance_value.adjustSize()

        return True

    def set_currency_type_gui(self, currency_type):
        self.label_currency_type_value.setText(currency_type)
        self.label_currency_type_value.adjustSize()

        return True
    # End of: Mutator Funcions ---------------------------------------------------------------------------------------------------

    # Accessor Functions ----------------------------------------------------------------------------------------------------------
    def get_balance_online(self):
        self.balance = self.Plutus.get_balance()

        return self.balance

    def get_balance_local(self):
        return self.balance

    def get_currency_type_online(self):
        self.currency_type = self.Plutus.get_currency()

        return self.currency_type()

    def get_currency_type_local(self):
        return self.currency_type
    # End of: Accessor Functions --------------------------------------------------------------------------------------------------

    # Utility Functions -----------------------------------------------------------------------------------------------------------
    def connect(self):
        self.is_connected, self.connection_status_reason = self.Plutus.connect()    # Connect to iq option server.

        if self.is_connected:
            print("######### [ Success ] >>  Re-connection Attempt to the iq option Server #########")

            return True
        else:
            print("#########", self.connection_reason, "#########")

            return False

    def check_connection(self):
        return self.Plutus.check_connect()

    def refresh_everything(self):
        return True

    def reset_balance(self):
        self.Plutus.reset_practice_balance()
        self.balance = self.get_balance_online()

        print("#########", self.balance, "#########")

        self.label_balance_value.setText(str(self.balance))

        return self.balance

    def get_iq_option_API_version(self):
        return IQ_Option.__version__
    
    def get_server_timestamp(self):
        return self.Plutus.get_server_timestamp()
    # End of: Utility Functions ---------------------------------------------------------------------------------------------------


def main():
    Plutus = Logic()

    current_local_time = str(time.ctime()).replace(":", "-")
    log_file_name = current_local_time + " iq_option_connection"

    """
    logging.basicConfig(filename="logs/" + log_file_name + ".log",
                        format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
                        # datefmt="%H:%M:%S",
                        level=logging.DEBUG)    # Debug mode on
    """

    logging.basicConfig(format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
                        # datefmt="%H:%M:%S",
                        level=logging.DEBUG)    # Debug mode on

    # Initialize
    Plutus = IQ_Option(test_accounts["email_1"], test_accounts["password_1"])

    # Default User-Agent is "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
    header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:70.0 Gecko/20100101 Firefox/70.0"}
    cookie = {"Plutus": "GOOD"}

    Plutus.set_session(header, cookie)

    # First connection attempt to the iq option server.
    is_connected, connection_status_reason = Plutus.connect()

    if is_connected:
        print("######### [ Success ] >> First Connection Attempt to the iq option Server #########")


        initial_data = {
            "iq_option_API_version": "",    # IQ_Option.__version__
            "is_connected": Plutus.check_connect(),    # Plutus.check_connect()
            "connection_status_reason": connection_status_reason,
            "server_timestamp": Plutus.get_server_timestamp(),    # Plutus.get_server_timestamp()

            "digital_option_name": "live-deal-digital-option",    # "live-deal-digital-option" / "live-deal-binary-option-placed"
            "digital_option_active": "EURUSD",    # And much more
            "digital_option_type": "PT1M",    # "PT1M" / "PT5M" / "PT15M"
            "digital_option_buffer_size": 10,    # I do not know what this is.

            "binary_option_name": "live-deal-binary-option-placed",    # "live-deal-digital-option" / "live-deal-binary-option-placed"
            "binary_option_active": "EURUSD",    # And much more
            "binary_option_type": "turbo",    # "turbo" / "binary"
            "binary_option_buffer_size": 10,    # I do not know what this is.

            "balance_type": "PRACTICE",    # "PRACTICE" / "REAL"
            "balance": "Plutus.get_balance()",    # Plutus.get_balance()
            "currency_type": "Plutus.get_currency()"    # Plutus.get_currency()
        }

        # Pyhton GUI Initialization
        app = QApplication(sys.argv)
        window = Window(Plutus, initial_data)

        sys.exit(app.exec_())
    else:
        print("######### [ FAIL ] >> First Connection Attempt to the iq option Server #########")
        print("######### [ REASON ] >>", connection_status_reason, "#########")


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
