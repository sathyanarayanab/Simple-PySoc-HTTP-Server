from threading import Thread
import socket
import mimetypes
import urllib
import os

magic = "\xFE"
defaulthtml = """HTTP/1.1 200 OK
Connection: Keep-Alive
Content-Type: {type}
Accept-Ranges: bytes
Vary: Accept-Encoding
Server: Apache/2.4.41 (Ubuntu)

{body}"""


defaultcss = """HTTP/1.1 200 OK
Content-Type: text/css
Accept-Ranges: bytes
Server: Apache/2.4.41 (Ubuntu)
{body}
"""

defaultjs = """HTTP/1.1 200 OK
Content-Type: text/js
Accept-Ranges: bytes
Server: Apache/2.4.41 (Ubuntu)
{body}
"""

defaultimg = """HTTP/1.1 200 OK
Content-Type: text/js
Accept-Ranges: bytes
Server: Apache/2.4.41 (Ubuntu)
{body}
"""

def checkfiletype(file):
    return mimetypes.guess_type(file)


class newThread(Thread):
    def __init__(self, conn,addr):
        Thread.__init__(self)
        self.addr = addr
        self.conn = conn
        print("Thread started\n")

    def run(self):
        while True:
            data = self.conn.recv(4096).decode().split('\n')[0]
            file = data.split(" ")[1]
            if(file=="/"):
                file= "index.html"
            else:
                file = str(file).replace("/","")
            filetype = checkfiletype(file)
            if str(filetype).find("image")!= -1: # Image sending is Work in progress, Image will not be loading in HTML page, please feel free to let me know why it happens
                with open(file, 'rb') as f:
                    l = os.path.getsize(file)
                    body = f.read(1)
                    self.conn.sendall(defaulthtml.format(body=body,type=filetype[0]).encode())
                    f.close()
            else:
                with open(file, 'rt') as f:
                    body = f.read()
                    f.close()
                    self.conn.sendall(defaulthtml.format(body=body,type=filetype[0]).encode('utf-8'))
            self.conn.close()


            
            


HOST = "0.0.0.0"
PORT = 1234

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind((HOST,PORT))
s.listen()
while True:
    print("Starting\n")
    conn, addr = s.accept()
    print("Started\n")
    newThread(conn,addr).start()
