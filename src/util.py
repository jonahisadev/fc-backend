from datetime import datetime

def getTime():
    time = datetime.now()
    fmt = datetime.strptime("%02d:%02d" % (time.hour, time.minute), "%H:%M")
    nfmt = fmt.strftime("%I:%M %p")
    return "[%s]" % nfmt 