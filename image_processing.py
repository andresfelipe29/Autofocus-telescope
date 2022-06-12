import cv2

#calback function for trackbars

a_c = 0
b_c = 0
def parameter_a(x):
	print(x," ", b_c, "\t",canny_var_i-canny_var_o)
def parameter_b(x):
	print(a_c," ", x, "\t",canny_var_i-canny_var_o)

#read images and set greyscale
img_o = cv2.imread("car1.jpg", cv2.IMREAD_GRAYSCALE)
img_i = cv2.imread("car2.jpg", cv2.IMREAD_GRAYSCALE)

#create border images with laplacian and save contrast values
laplacian_o = cv2.Laplacian(img_o, cv2.CV_64F)
laplacian_var_o = cv2.Laplacian(img_o, cv2.CV_64F).var()
laplacian_i = cv2.Laplacian(img_i, cv2.CV_64F)
laplacian_var_i = cv2.Laplacian(img_i, cv2.CV_64F).var()

#create border images with canny and save contrast values
canny_o = cv2.Canny(img_o,100,200)
canny_var_o = cv2.Canny(img_o,100,200).var()
canny_i = cv2.Canny(img_i,100,200)
canny_var_i = cv2.Canny(img_i,100,200).var()

#windows on which the trackbar will be added
cv2.namedWindow("Canny_o")

#trackbars setup
cv2.createTrackbar('A_c', "Canny_o", 100, 200, parameter_a)
cv2.createTrackbar('B_c', "Canny_o", 200, 300, parameter_b)

#print(laplacian_var_o)
print(laplacian_var_i-laplacian_var_o)
#print(canny_var_o)
print(canny_var_i-canny_var_o)

#display
while(1):
	cv2.imshow("Laplacian_o", laplacian_o)
	cv2.imshow("Canny_o", canny_o)
	cv2.imshow("Laplacian_i", laplacian_i)
	cv2.imshow("Canny_i", canny_i)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

	a_c = cv2.getTrackbarPos("A_c", "Canny_o")
	b_c = cv2.getTrackbarPos("B_c", "Canny_o")

	canny_o = cv2.Canny(img_o,a_c,b_c)
	canny_var_o = cv2.Canny(img_o,a_c,b_c).var()
	canny_i = cv2.Canny(img_i,a_c,b_c)
	canny_var_i = cv2.Canny(img_i,a_c,b_c).var()
	
cv2.destroyAllWindows()
