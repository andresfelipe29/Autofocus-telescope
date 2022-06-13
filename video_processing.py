import cv2
import time
import math
import serial

#set communication
port = "COM3"
ser = serial.Serial(port, 9600, timeout=1)

#read video
raw_video = cv2.VideoCapture(0)

#threshold
threshold_up = 600
threshold_down = 12

#state varibles
onOffState = "on"
directionState = "cl"
prev_directionState = "cl"
state = onOffState+" "+directionState

#tell arduino we need to focus
ser.write(state.encode())
time.sleep(0.5)

start = time.time()
ser.write(state.encode())
time.sleep(0.5)
partial = time.time() - start
print('\n', ser.readline().decode('ascii').strip(), 'at', partial)

#timer
previous = 0
seconds = 1
start = time.time()

#conditions
focused = 0

#display
while True:
	#read time
	partial = time.time() - start
	current = int(math.floor(partial))
	
	#grayscale filter
	ret, frame = raw_video.read()
	gray_video = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	#create border images with canny and save contrast values
	canny = cv2.Canny(gray_video,0,100)
	cv2.imshow("Canny", canny)
	canny_var = cv2.Canny(gray_video,0,100).var()

	#show canny's result every 'seconds'
	if (current % seconds == 0) and (current != previous):
		print(round(partial,3), "\t", current, "\t", previous, "\t", round(canny_var,3))
		previous = current

	#go back when threshhold_up is reached
	if (canny_var > threshold_up):
		directionState = "co"
		if ((onOffState == "on") and (directionState != prev_directionState)):
			prev_directionState = directionState
			state = onOffState+" "+directionState
			ser.write(state.encode())
			time.sleep(1)
			partial = time.time() - start
			print('\n', ser.readline().decode('ascii').strip(), 'at', partial)

	#go forward when threshold_down is reached
	if (canny_var < threshold_down):
		directionState = "cl"
		if (onOffState == "on" and directionState != prev_directionState):
			prev_directionState = directionState
			state=onOffState+" "+directionState
			ser.write(state.encode())
			time.sleep(1)
			partial = time.time() - start
			print('\n', ser.readline().decode('ascii').strip(), 'at', partial)        	

	if cv2.waitKey(1) & 0xFF == ord('q'):
		ser.write("of cl".encode())
		break

raw_video.release()
cv2.destroyAllWindows()
ser.close()