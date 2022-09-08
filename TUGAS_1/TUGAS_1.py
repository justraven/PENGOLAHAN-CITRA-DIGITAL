import cv2 as cv

image = cv.imread('lena.jpg')

lebar = int(image.shape[0] * 80/100)
panjang = int(image.shape[1] * 40/100)

image = cv.resize(image,(lebar,panjang))

cv.imshow('original image',image)

R = (image[:,:,2])
G = (image[:,:,1])
B = (image[:,:,0])

RGB2G_formula = 0.2989 * R + 0.5870 *G + 0.1140 * B

ret,biner_image = cv.threshold(RGB2G_formula,128,128,cv.THRESH_TOZERO_INV)
ret,biner_image_ = cv.threshold(biner_image,90,90,cv.THRESH_TOZERO)

cv.imshow("binary",biner_image_)

cv.waitKey(0)
cv.destroyAllWindows()