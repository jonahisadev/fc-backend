import thread
import time
import sys

def getInput():
    while True:
        cmd = raw_input("")
        print("You said '%s'" % cmd)
        if (cmd == "exit"):
            thread.interrupt_main()

def main():
    thread.start_new_thread(getInput, ())
    
    while True:
        try:
            print("Hi")
            time.sleep(2)
        except KeyboardInterrupt:
            break
        
        
if __name__ == "__main__":
    main()