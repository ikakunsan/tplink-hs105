#
# Sample program to to check the library
#
# 2022 ikakunsan
#

from ipaddress import ip_address
from tplink_hs105 import HS105Exception, TPLinkHS105
import time

# Specify IP address of the device
# Please replace with the address of your device
ipaddr = "192.168.12.34"

hs105_1 = TPLinkHS105(ipaddr)

try:
    # Get the device status
    r = hs105_1.get_all_info()
    print("\n", r)
    print("\nAlias Name:", hs105_1.get_alias())
    print("\nOutlet Statue:", hs105_1.get_outlet_status())

    # Wait for a while for next action
    time.sleep(3)

    # Turn on the outlet
    r = hs105_1.outlet_on()
    print("\nOutlet Statue:", hs105_1.get_outlet_status())

    # Wait for a while for next action
    time.sleep(3)

    # Turn off the outlet
    r = hs105_1.outlet_off()
    print("\nOutlet Statue:", hs105_1.get_outlet_status())

except HS105Exception as e:
    print(e)
