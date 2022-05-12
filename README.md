# tplink-hs105
A simple Python library for TP-Link HS105

## Overview
A simple Python library for TP-Link HS105, that works on MicroPython.
You should use Python-Kasa for Python 3. It's much better solution. 😄

## Requirements
- Python 3.x (Checked with v3.10)
- MicroPython (Checked with v1.18 on ESP32)

## Usage
    from tplink_hs105 import HS105Exception, TPLinkHS105
    hs = TPLinkHS105(ipaddr)
    r = hs105_1.outlet_on()
Refer to the example for the usage.
