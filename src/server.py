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
    
    # Checks server commands (separate thread)
    def commands(self):
        while True:
            cmd = raw_input("")
            if (cmd == "quit"):
                # Call cleanups
                os._exit(0)
            else:
                print("Unknown command: '%s'" % cmd)
    
    # Print to server log            
    def log(self, msg):
        print("%s %s" % (util.getTime(), msg))
    
    # Send data to specified host/port    
    def sendData(self, msg, addr, port):
        self.sock.sendto(msg, (addr, port))
    
    # Check if username exists    
    def nameExists(self, name):
        for conn in self.conns:
            if (conn.name == name):
                return True
        return False
    
    # Get username by IP and port    
    def getNameByIP(self, host, port):
        for conn in self.conns:
            if (conn.addr == host and conn.port == port):
                return conn.name
        return None
    
    # Get connection list index by username    
    def getIndexByName(self, name):
        i = 0
        for conn in self.conns:
            if (conn.name == name):
                break
            i += 1
        return i
    
    # Broadcast to every connection    
    def broadcast(self, msg):
        for conn in self.conns:
            self.sendData(msg, conn.addr, conn.port)
    
    # Main server loop
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
                #   /c/: Connection request
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
                #   /m/: User broadcast message
                #    
                elif (args[0] == "/m/"):
                    name = self.getNameByIP(host, port)
                    self.log("[%s]: %s" % (name, args[1]))
                    self.broadcast("/m/~%s~%s" % (name, args[1]))
                        
                #
                #   /x/: Disconnection
                #
                elif (args[0] == "/x/"):
                    name = self.getNameByIP(host, port)
                    self.log("%s disconnected." % name)
                    self.broadcast("/s/~%s disconnected." % name)
                    del self.conns[self.getIndexByName(name)]
                    
            except KeyboardInterrupt:
                break
