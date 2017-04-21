import sys
from server import Server

def main():
    if (sys.argv[1] == "server"):
        server = Server("localhost", 33333)
        server.start()
        
if __name__ == "__main__":
    main()