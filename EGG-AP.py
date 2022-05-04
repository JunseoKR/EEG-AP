import serial
import threading
import time

# Arduino Set
port = "COM5"
baud = "230400"
ser = serial.Serial(port, baud, timeout=1)

# Threading
def main():
    thread = threading.Thread(target=Input, args=(ser,))
    thread.start()

# Buffer Input
def Input(ser):
    while True:
        if ser.readable():
            res = ser.readline()
            print(res)
    
    ser.close()

# Main Section
main()