#import serial
ser = serial.Serial('/dev/ttyUSB0', 19200)

while 1:
    if(ser.inWaiting()>0):
        myData = ser.readline()
        print myData
