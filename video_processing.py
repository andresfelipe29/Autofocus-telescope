import cv2
import time
import math
import serial

#set communication
port = 'COM3'
ser = serial.Serial(port, 9600, timeout=1)

#read video
raw_video = cv2.VideoCapture(0)

#timer
start = time.time()
previous = 0
seconds = 1

#threshold
threshold = 500

#display
while True:	
	#read time
	partial = time.time() - start
	current = int(math.floor(partial))
	
	#tell arduino we need to focus
	if (previous == 0):
		focusing = 'on'
		ser.write(focusing.encode())
		time.sleep(0.5)
		print(ser.readline().decode('ascii'))

	#grayscale filter
	ret, frame = raw_video.read()
	gray_video = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	#create border images with canny and save contrast values
	canny_var = cv2.Canny(gray_video,0,100).var()
	canny = cv2.Canny(gray_video,0,100)
	cv2.imshow("Canny", canny)

	#show canny's result every 'seconds'
	if (current % seconds == 0) and (current != previous):
		print(round(partial,3), "\t", current, "\t", previous, "\t",\
	              round(canny_var,3))
		previous = current

	#stop focusing when threshold is reached
	
	if (canny_var > threshold):
		focusing = 'done'
		ser.write(focusing.encode())
		time.sleep(0.5)
		print('\n', ser.readline().decode('ascii').strip(), 'at', partial)
		break

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

raw_video.release()
cv2.destroyAllWindows()
ser.close()