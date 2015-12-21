"""
quicknet: do simple 'net' (TCP, HTTP, HTTPS, ...) operations from the commands line
          for both the sending and receiving flows.

Meant as a simple tool to hack things together when you want to leverage python's libs.
If you are using only HTTP(S), you might want to take a look at 'curl' as well, this script is more useful if you just want to poke a server with TCP.

# TODO
# Bugs

"""

import time
import pdb
import argparse
import socket
import sys
import ssl
import os
import http.client
import http.server
import socketserver

from urllib.parse import urlparse
from random import randint

_meta_shell_command = 'quicknet'

def getArgs():
    
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    defaultPayload = "Test payload 1234."
    
    parser.add_argument('-d', '--direction', type = str, default = "send", help="send or recv")
    parser.add_argument('-s', '--scheme', type = str, default = "tcp", help="tcp, udp, http or https")
    parser.add_argument('-t', '--target', type = str, default = "127.0.0.1", help="Target IP or FQDN.")
    parser.add_argument('-p', '--port', type = int, default = 8000, help="Port.")
    parser.add_argument('-b', '--payload', nargs = '*', type = str, default = defaultPayload, help="Payload as a string. Space separated is fine.")
    parser.add_argument('-f', '--file_payload', type = str, default=None, help="File name that is loaded and sent as payload.")
    #parser.add_argument('--file_payload_lines', type = str, default = None, help="")
    parser.add_argument('--fuzz_payload', action="store_true", default = False, help="")
    parser.add_argument('--special', action="store_true", default = False, help="Run some hard-coded function.")
    
    args = parser.parse_args()
    
    if args.file_payload is not None:
        assert args.payload == defaultPayload
        args.payload = None
    
    return args

def udpSend(ip, payload):

    if False:
        payload = payload.replace("\\n", "\n")
        payload = payload.replace("\\r", "\r")
        payload = payload.replace("\\0", "\0")
    
    print('udpSend %s %s' % (ip, payload))
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    ip, port = ip.split(':')[0], int(ip.split(':')[1])
    
    if type(payload) != type(b''):
        payload = payload.encode()
    sock.sendto(payload, (ip, port))
   
def special():
    payload = """POST /config?command=light HTTP/1.1

{"red":0}
    """
    #tcpSend("192.168.1.11:80", payload)
    while 1:
        try:
            hc = http.client.HTTPConnection('192.168.1.11:80')
            hc.request("POST", "/config?command=light", body=r'{"red":0}')
            resp = hc.getresponse()
            print("%s %s" % (resp.status, resp.reason))

            hc = http.client.HTTPConnection('192.168.1.11:80')
            hc.request("POST", "/config?command=light", body=r'{"red":1}')
            resp = hc.getresponse()
            print("%s %s" % (resp.status, resp.reason))

            time.sleep(1)
        except:
            time.sleep(5)

def tcpSend(ip, port, payload):
    
    if False:
        payload = payload.replace("\\n", "\n")
        payload = payload.replace("\\r", "\r")
        payload = payload.replace("\\0", "\0")
        
        if payload.find('|||') != -1:
            payload = payload.split('|||')
        else:
            payload = [payload]

    #ip, port = ip.split(':')[0], int(ip.split(':')[1])        
    
    #for pp in payload:
    
    print('tcpSend %s %s' % (ip, payload))
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5.00)
    s.connect((ip, port))
    
    payload = payload.encode()
    print('Sending: %s.' % payload)
    if type(payload) != type(b''):
        payload = payload.encode()
    s.send(payload)

    recv = s.recv(1024)
    print('Recv: %s.' % recv)
    
    s.close()
    
def tcpRecv(port):
    print('Starting TCP listening on ', locals())
    while True:
        try:
            host = '0.0.0.0'
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(15.00)
            print('bind on', host, port)
            s.bind((host, port))
            s.listen(1)
            conn, addr = s.accept()
            print('Connected to: ', addr)
            conn.setblocking(False)
            conn.settimeout(5) # in seconds
            allData = []
            
            while 1:
                data = conn.recv(1024) # if < 1024, this still returns with whatever was sent in the frame.
                data = data.decode()
                allData.append(data)
                print('Recv chunk:\n', data)
                if len(allData) > 1:
                    print('All %i chunks collated:\n%s' % (len(allData), "".join(allData)))
            
        except socket.timeout as e:
            print('Timed-out, dumped connection and listening again.')
        except Exception as e:
            print("Exception: ", e)
        finally:
            conn.close()

def httpRecv(port, isHttps = False):

    class MyHttpHandler(http.server.BaseHTTPRequestHandler):

        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "application/json;charset=utf-8")

            r="<h1>Hello World</h1>"
            self.send_header("Content-length", len(r))
            self.end_headers()
            self.wfile.write(r.encode("utf-8"))
            self.wfile.flush()
            
        def do_POST(self):
            
            self.send_response(200)
            self.send_header("Content-type", "application/json;charset=utf-8")
            
            if self.headers['content-length'] is not None:
                print('Try read...')
                length = int(self.headers['content-length']) 
                recv = self.rfile.read(length)
                print('RECV:\n', recv)
            
            self.end_headers()
    
    if isHttps: sScheme = 'HTTPS'
    else: sScheme = 'HTTP'
    
    print('Starting %s listening on %s.' % (sScheme, port))
    
    httpd = socketserver.TCPServer(("", port), MyHttpHandler)
    
    if isHttps:
        httpd.socket = ssl.wrap_socket(httpd.socket,
                                    server_side=True,
                                    certfile= r't:\temp\test_certs.pem')
                                    #,cert_reqs=ssl.CERT_NONE)
                                
    print("Serving at port", port)
    httpd.serve_forever()
    
def httpsRequestResponse(fqdn, payload):
    
    parsedFqdn = urlparse(fqdn)
    
    #context = ssl.create_default_context()
    #context = ssl.SSLContext(ssl.CERT_NONE) # Do not verify server's certs.
    context = ssl.SSLContext(ssl.CERT_OPTIONAL)
    
    ttt = parsedFqdn.netloc
    if ttt.find(':') != -1:
        ttt = ttt.split(':')[0]
    
    conn = http.client.HTTPSConnection(ttt, parsedFqdn.port, context=context)
    conn.request("GET", parsedFqdn.path)

    print(conn.getresponse().read())
    
if __name__ == '__main__':
    
    args = getArgs()
    payload = None
    
    print(args)
    if args.special is True:
        special()
        sys.exit(0)

    if args.file_payload is not None:
        
        fh = open(args.file_payload, 'rb')
        payload = fh.read()
        fh.close()
    else:
        if(type(args.payload) == type([])):
            payload = " ".join(args.payload)
        else:
            payload = args.payload
    
    if args.fuzz_payload is True:
        
        bytes = []
        length = randint(10, 1000)
        payload = os.urandom(length)
        
    if args.scheme == "udp" and args.direction == "send":
        if type(payload) == type([]):
            for p in payload:
                udpSend(args.target, p)
        else:
            udpSend(args.target, payload)
        sys.exit(0)
    
    if args.scheme == "tcp" and args.direction == "send":
        """
        if type(payload) == type([]):
            for p in payload:
                tcpSend(args.target, p)
        else:    
        """
        tcpSend(args.target, args.port, payload)
        sys.exit(0)
        
    if args.scheme == "https" and args.direction == "send":
        httpsRequestResponse(args.target, payload)
        sys.exit(0)        
    
    if args.scheme == "tcp" and args.direction == "recv":
        tcpRecv(args.port)        
        sys.exit(0)
       
    if args.scheme == "http" and args.direction == "recv":
        httpRecv(args.port)
        sys.exit(0)
    
    if args.scheme == "https" and args.direction == "recv":
        httpRecv(args.port, isHttps = True)
        sys.exit(0)    
    
    raise Exception("Invalid command-line.")
    
