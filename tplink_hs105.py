#
# Simple TP-link HS105 control library
#
# 2022 ikakunsan
#
import socket
import struct
import json

TCP_PORT = 9999
TIMEOUT = 5
INIT_KEY = 171

class HS105Exception(Exception):
    pass

class TPLinkHS105:
    def __init__(self, ipaddr: str):
        self._ip_addr = ipaddr

    @staticmethod
    def _encrypt(plaintext: str) -> bytes:
        key = INIT_KEY
        r = struct.pack(">I", len(plaintext))
        for c in plaintext.encode("utf-8"):
            bout = key ^ c
            key = bout
            r += bytes([bout])
        return r

    @staticmethod
    def _decrypt(ciphertext: bytes) -> str:
        key = INIT_KEY
        r = ""
        for c in ciphertext:
            bout = key ^ c
            key = c
            r += chr(bout)
        return r

    @staticmethod
    def _send_command(ipaddr: str, cmd: str) -> str:
        try:
            sock = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM
            )  # SOCK_STREAM for TCP
            sock.settimeout(TIMEOUT)
            sock.connect((ipaddr, TCP_PORT))
            sock.send(TPLinkHS105._encrypt(cmd))
            ack = sock.recv(2048)
            sock.close()
            r = TPLinkHS105._decrypt(ack[4:])
        except socket.error as e:
            raise HS105Exception(f'Connection Error: {e} ({ipaddr})')
        return r

    # Get all device information
    def get_all_info(self) -> str:
        cmd = '{"system":{"get_sysinfo":{}}}'
        r = TPLinkHS105._send_command(self._ip_addr, cmd)
        return r

    # Get alias name (can be set by KASA app)
    def get_alias(self) -> str:
        cmd = '{"system":{"get_sysinfo":{}}}'
        r = TPLinkHS105._send_command(self._ip_addr, cmd)
        if r != "error":
            r = json.loads(r)["system"]["get_sysinfo"]["alias"]
        return r

    # Get outlet status. 1:ON, 0:OFF
    def get_outlet_status(self) -> bool:
        cmd = '{"system":{"get_sysinfo":{}}}'
        r = TPLinkHS105._send_command(self._ip_addr, cmd)
        if r != "error":
            r = json.loads(r)["system"]["get_sysinfo"]["relay_state"]
        return r

    # Turn on the outlet. Return: JSON from the device
    def outlet_on(self) -> str:
        # set_relay_state: 1
        cmd = '{"system":{"set_relay_state":{"state":1}}}'
        r = TPLinkHS105._send_command(self._ip_addr, cmd)
        return r

    # Turn off the outlet: JSON from the device
    def outlet_off(self) -> str:
        # set_relay_state: 0
        cmd = '{"system":{"set_relay_state":{"state":0}}}'
        r = TPLinkHS105._send_command(self._ip_addr, cmd)
        return r

    # Reboot the device
    def reboot(self) -> str:
        cmd = '{"system":{"reboot":{"delay":1}}}'
        r = TPLinkHS105._send_command(self._ip_addr, cmd)
        return r

    # Factory reset the device (TOO DANGER)
    # def reset(self) -> str:
    #    cmd = '{"system":{"reset":{"delay":1}}}'
    #    r = TPLinkHS105._send_command(self._ip_addr, cmd)
    #    return r
