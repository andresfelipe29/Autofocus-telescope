import serial
import time

ser = serial.Serial('COM3', 9600, timeout=1)
onOffState = "off"
directionState = "cl"

while True:
    onOffState, directionState = input("on/off, cl/co: ").split()
    if not (onOffState in {"on", "off"} and directionState in {"cl", "co"}):
        print("invalid input, please try again")
        continue

    start = time.time()
    #setting the message for proper reading in arduino
    if (onOffState == "on"):
        state = onOffState+" "+directionState
        ser.write(state.encode())
    else:
        state = onOffState[:-1]+" "+directionState
        ser.write(state.encode()) 
    time.sleep(0.1)
    print(ser.readline().decode('ascii'))
    print(round(time.time() - start,3))

ser.close()