from iqoptionapi.stable_api import IQ_Option
import time
from accounts import test_accounts

# Debug mode on
import logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(message)s")

# Global variables
balance_type = "PRACTICE"   # "PRACTICE" / "REAL"

digital_option_name = "live-deal-digital-option"    # "live-deal-digital-option" / "live-deal-binary-option-placed"
digital_option_active = "EURUSD"    # And much more
digital_option_type = "PT1M"    # "PT1M" / "PT5M" / "PT15M"
digital_option_buffer_size = 10    # I do not know what this is.

binary_option_name = "live-deal-binary-option-placed"    # "live-deal-digital-option" / "live-deal-binary-option-placed"
binary_option_active = "EURUSD"    # And much more
binary_option_type = "turbo"    # "turbo" / "binary"
binary_option_buffer_size = 10    # I do not know what this is.

# Utility variables
error_password = "{"\
    "\"code\":\"invalid_credentials\","\
    "\"message\":\"You entered the wrong credentials. Please check that the login/password is correct.\""\
"}"

Plutus = IQ_Option(test_accounts["email_1"], test_accounts["password_1"])

# Default User-Agent is "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:70.0 Gecko/20100101 Firefox/70.0"}
cookie = {"Plutus": "GOOD"}

Plutus.set_session(header, cookie)

check, reason = Plutus.connect()    # First connection attempt to iq option.
print("######### Connection Status #########", check, reason, "######### Connection Status #########")

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

iq_option_API_version = IQ_Option.__version__
server_connection_status = Plutus.check_connect()
server_timestamp = Plutus.get_server_timestamp()

print("######### iq option API Version #########", iq_option_API_version, "######### iq option API Version #########")
print("######### Connection Status #########", server_connection_status, "######### Connection Status #########")
print("######### Server Time #########", server_timestamp, "######### Server Time #########")

# =========================================================================================================================
# Account
# =========================================================================================================================
balance = Plutus.get_balance()
print("######### Balance #########", balance, "######### Balance #########")

# Plutus.get_balance_v2()    # Not working.
# print("######### Balance v2 #########", balance_v2, "######### Balance v2 #########")

currency = Plutus.get_currency()
print("######### Currency #########", currency, "######### Currency #########")

# print(Plutus.reset_practice_balance())

# =========================================================================================================================
# End of: Account
# =========================================================================================================================

"""
goal = "EURUSD"
print("get candles")
print(Plutus.get_candles(goal, 60, 111, time.time()))
"""
