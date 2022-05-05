import serial
import threading
import time

# Arduino Set
port = "COM5"
baud = "230400"
# Serial Connection
ser = serial.Serial(port, baud, timeout=1)

# Threading
def main():
    thread = threading.Thread(target=Connection, args=(ser,))
    thread.start()

# Buffer Input
def Connection(ser):
    while True:
        if ser.readable():
            res = ser.readline()
            print(res.decode()[:len(res)])
    
    ser.close()

# Main Section
main()