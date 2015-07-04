"""
Disregard this file, as of now it is just tests.
"""

import argparse
import socket
import sys
import os
import http.client
import ssl

from urllib.parse import urlparse
from random import randint

_meta_shell_command = 'dns'

udpPayloadHexStream = '338a01000001000000000000037777770667726f6b69740263610000010001'
udpPayload = udpPayloadHexStream.decode("hex")

def udpSend(ip, payload):
    
    print('udpSend %s %s' % (ip, payload))
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    ip, port = ip.split(':')[0], int(ip.split(':')[1])
    
    if type(payload) != type(b''):
        payload = payload.encode()

    sock.sendto(payload, (ip, port))

ip = '192.112.36.4'

