import sys
from server import Server

def main():
    server = Server(sys.argv[1], int(sys.argv[2]))
    server.start()
        
if __name__ == "__main__":
    main()