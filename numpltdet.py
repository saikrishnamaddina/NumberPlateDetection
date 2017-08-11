import cv2
import sys
import numpy as np

#.........Read image..........#

img = cv2.imread(sys.argv[1],1)
# Creating a Named window to display image
#cv2.namedWindow("original image",cv2.WINDOW_NORMAL)
# Display image
cv2.imshow("Original Image",img)
cv2.waitKey(0)


# RGB to Gray scale conversion

img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#cv2.namedWindow("Gray Converted Image",cv2.WINDOW_NORMAL)
#cv2.imshow("Gray Converted Image",img_gray)
#cv2.waitKey(0)

# Noise removal with iterative bilateral filter(removes noise while preserving edges)

noise_removal = cv2.bilateralFilter(img_gray,9,75,75)
#cv2.namedWindow("Noise Removed Image",cv2.WINDOW_NORMAL)
#cv2.imshow("Noise Removed Image",noise_removal)
#cv2.waitKey(0)


# Histogram equalisation for better results

equal_histogram = cv2.equalizeHist(noise_removal)
#cv2.namedWindow("After Histogram equalisation",cv2.WINDOW_NORMAL)
#cv2.imshow("After Histogram equalisation",equal_histogram)
#cv2.waitKey(0)

# Morphological opening with a rectangular structure element

kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
morph_image = cv2.morphologyEx(equal_histogram,cv2.MORPH_OPEN,kernel,iterations=15)
#cv2.namedWindow("Morphological opening",cv2.WINDOW_NORMAL)
#cv2.imshow("Morphological opening",morph_image)
#cv2.waitKey(0)

# Image subtraction(Subtracting the Morphed image from the histogram equalised Image)

sub_morp_image = cv2.subtract(equal_histogram,morph_image)
#cv2.namedWindow("Subtraction image", cv2.WINDOW_NORMAL)
#cv2.imshow("subtraction image",sub_morp_image)
#cv2.waitKey(0)

# Thresholding the image

ret,thresh_image = cv2.threshold(sub_morp_image,0,255,cv2.THRESH_OTSU)
#cv2.namedWindow("Image after Thresholding",cv2.WINDOW_NORMAL)
#cv2.imshow("Image after Thresholding",thresh_image)
#cv2.waitKey(0)

# Applying Canny Edge detection

canny_image = cv2.Canny(thresh_image,250,255)
#cv2.namedWindow("Image after applying Canny",cv2.WINDOW_NORMAL)
#cv2.imshow("Image after applying Canny",canny_image)
#cv2.waitKey(0)
canny_image = cv2.convertScaleAbs(canny_image)

# dilation to strengthen the edges

kernel = np.ones((3,3), np.uint8)
dilated_image = cv2.dilate(canny_image,kernel,iterations=1)
#cv2.namedWindow("Dilation", cv2.WINDOW_NORMAL)
#cv2.imshow("Dilation", dilated_image)
#cv2.waitKey(0)

# Finding Contours in the image based on edge

(image,contours, hierarchy) = cv2.findContours(dilated_image,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
contours= sorted(contours, key = cv2.contourArea, reverse = True)[:10]
screenCnt = None
for c in contours:
 peri = cv2.arcLength(c, True)
 approx = cv2.approxPolyDP(c, 0.06 * peri, True)  # Approximating with 6% error
 if len(approx) == 4:  # Select the contour with 4 corners
  screenCnt = approx
  break
cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)
#cv2.namedWindow("Image with Selected Contour",cv2.WINDOW_NORMAL)
cv2.imshow("Image with Selected Contour",img)
cv2.waitKey(0)

# Masking the part other than the number plate

mask = np.zeros(img_gray.shape,np.uint8)
new_image = cv2.drawContours(mask,[screenCnt],0,255,-1,)
new_image = cv2.bitwise_and(img,img,mask=mask)
#cv2.namedWindow("Final_image",cv2.WINDOW_NORMAL)
cv2.imshow("Final_image",new_image)
cv2.waitKey(0)

# Histogram equal for enhancing the number plate for further processing

y,cr,cb = cv2.split(cv2.cvtColor(new_image,cv2.COLOR_BGR2YCR_CB))
y = cv2.equalizeHist(y)
final_image = cv2.cvtColor(cv2.merge([y,cr,cb]),cv2.COLOR_YCR_CB2BGR)

# Merging the 3 channels

cv2.namedWindow("Enhanced Number Plate",cv2.WINDOW_NORMAL)
cv2.imshow("Enhanced Number Plate",final_image)
cv2.waitKey(0) # Wait for a keystroke from the user
