import serial

ser = serial.Serial('/dev/ttyS2', 9600, timeout=1)

while True:
    case = input()
    if (case == '1'):
        ser.write(b'1')
    elif (case == 'stop'):
        print('breaking communication\n')
        break
    else:
        print('invalid case, try again')
    
ser.close()
