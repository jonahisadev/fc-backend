import socket
import thread
import os
import util

from conn_info import ConnInfo

class Server:
    
    def __init__(self, addr, port):
        self.addr = addr
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((addr, port))
        
        self.conns = []
        
    def commands(self):
        while True:
            cmd = raw_input("")
            if (cmd == "quit"):
                # Call cleanups
                os._exit(0)
            else:
                print("Unknown command: '%s'" % cmd)
                
    def log(self, msg):
        print("%s %s" % (util.getTime(), msg))
        
    def sendData(self, msg, addr, port):
        self.sock.sendto(msg, (addr, port))
        
    def nameExists(self, name):
        for conn in self.conns:
            if (conn.name == name):
                return True
        return False
        
    def getNameByIP(self, host, port):
        for conn in self.conns:
            if (conn.addr == host and conn.port == port):
                return conn.name
        return None
    
    def start(self):
        print("Starting server on %s:%d" % (self.addr, self.port))
        thread.start_new_thread(self.commands, ())
        
        while True:
            try:
                data, addr = self.sock.recvfrom(1024)
                host = addr[0]
                port = addr[1]
                args = data.split("~")
                
                #
                #   /c/
                #
                if (args[0] == "/c/"):
                    if (not self.nameExists(args[1])):
                        self.conns.append(ConnInfo(host, port, args[1]))
                        self.log("%s connected" % args[1])
                        self.sendData("/c/~OK", host, port)
                    else:
                        self.log("Attempted login as '%s' from %s" % (args[1], host))
                        self.sendData("/c/~BADNAME", host, port)
                    
                #
                #   /m/
                #    
                elif (args[0] == "/m/"):
                    name = self.getNameByIP(host, port)
                    self.log("[%s]: %s" % (name, args[1]))
                    for conn in self.conns:
                        self.sendData("/m/~%s~%s" % (name, args[1]),
                        conn.addr, conn.port)
                    
            except KeyboardInterrupt:
                break
