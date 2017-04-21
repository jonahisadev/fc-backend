import sys
from server import Server

def showHelp():
    print("Server Help:")
    print("./run [addr] [port]: Start the server on the specified address and port")

def main():
    if (len(sys.argv) < 3):
        showHelp()
        sys.exit(1)
    
    server = Server(sys.argv[1], int(sys.argv[2]))
    server.start()
        
if __name__ == "__main__":
    main()