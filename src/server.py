import socket
import thread
import os
import util

class Server:
    
    def __init__(self, addr, port):
        self.addr = addr
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((addr, port))
        
    def commands(self):
        while True:
            cmd = raw_input("")
            if (cmd == "quit"):
                # Call cleanups
                os._exit(0)
                
    def log(self, msg):
        print("%s %s" % (util.getTime(), msg))
    
    def start(self):
        print("Starting server on %s:%d" % (self.addr, self.port))
        thread.start_new_thread(self.commands, ())
        
        while True:
            try:
                data, addr = self.sock.recvfrom(1024)
                args = data.split("~")
                
                if (args[0] == "/c/"):
                    self.log("%s connected" % args[1])
                    
                elif (args[0] == "/m/"):
                    self.log("[Somebody]: %s" % args[1])
                    
            except KeyboardInterrupt:
                break