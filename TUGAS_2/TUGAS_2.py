import cv2 as cv
import math
import numpy as np

image = cv.imread('lena.jpg')

lebar = int(image.shape[0] * 80/100)
panjang = int(image.shape[1] * 40/100)

image = cv.resize(image,(lebar,panjang))

#------------------------------------------- cara manual 
HSV_libray = cv.cvtColor(image, cv.COLOR_RGB2HSV)
RGB_library = cv.cvtColor(HSV_libray, cv.COLOR_HSV2RGB)
cv.imshow('HSV library',HSV_libray)
cv.imshow('RGB library', RGB_library)
#-------------------------------------------

#image yang diimport ke python memiliki format BGR
R = (image[:,:,2])
G = (image[:,:,1])
B = (image[:,:,0])

# ubah ke dalam ruang warna HSV
H = np.zeros([image.shape[0], image.shape[1]], dtype = float)
S = np.zeros([image.shape[0], image.shape[1]], dtype = float)
V = np.zeros([image.shape[0], image.shape[1]], dtype = float)
HSV = np.zeros((image.shape[0], image.shape[1], 3), 'uint8')


for i in range(image.shape[0]):
    for j in range(image.shape[1]):
        
        Bnorm = B[i][j]/float(255) # normalisasi
        Gnorm = G[i][j]/float(255)
        Rnorm = R[i][j]/float(255)

        Cmax = max(Bnorm, Gnorm, Rnorm) # nilai maksimum dari semua komponen warna
        Cmin = min(Bnorm, Gnorm, Rnorm) # nilai minimum dari semua komponen warna
        delta = Cmax - Cmin

        # hitung H
        if (delta == 0):
            H[i][j] = 0
        elif (Rnorm == Cmax):
            H[i][j] = (60*((Gnorm-Bnorm)/delta)+0 % 6)
        elif (Gnorm == Cmax):
            H[i][j] = (60*((Bnorm-Rnorm)/delta)+2 )
        elif (Bnorm == Cmax):
            H[i][j] = (60*((Rnorm-Gnorm)/delta)+4 )

        # hitung S
        if (Cmax == 0):
            S[i][j] = 0
        else:
            S[i][j] = (delta / Cmax) * 100

        # hitung V
        V[i][j] = Cmax*100

# menampilkan citra yang telah dibaca/import
H = H.astype('uint8')
S = S.astype('uint8')
V = V.astype('uint8')
HSV[..., 0] = H
HSV[..., 1] = S
HSV[..., 2] = V

cv.imshow('HSV Formula',HSV)

HSV = HSV.astype('float')
H = (HSV[:,:,0])
S = (HSV[:,:,1])
V = (HSV[:,:,2])

R = np.zeros([image.shape[0], image.shape[1]], dtype = float)
G = np.zeros([image.shape[0], image.shape[1]], dtype = float)
B = np.zeros([image.shape[0], image.shape[1]], dtype = float)
BGR = np.zeros((image.shape[0], image.shape[1], 3), 'uint8')

for i in range (HSV.shape[0]) :
    for j in range (HSV.shape[1]) :

        S[i][j] = S[i][j] / 100
        V[i][j] = V[i][j] / 100
        C = V[i][j] * S[i][j]
        X = C * (1 - abs(H[i][j]/60 % 2 - 1))
        m = V[i][j] - C

        if (H[i][j] >= 0 and H[i][j] < 60) :
            Red = C
            Green = X
            Blue = 0
        elif (H[i][j] >= 60 and H[i][j] < 120) :
            Red = X
            Green = C
            Blue = 0
        elif (H[i][j] >= 120 and H[i][j] < 180) :
            Red = 0
            Green = C
            Blue = X
        elif (H[i][j] >= 180 and H[i][j] < 240) :
            Red = 0
            Green = X
            Blue = C
        elif (H[i][j] >= 240 and H[i][j] < 300) :
            Red = X
            Green = 0
            Blue = C
        elif (H[i][j] >= 300 and H[i][j] < 360) :
            Red = C
            Green = 0
            Blue = X
        
        R[i][j] = (Red + m) * 255
        G[i][j] = (Green + m) * 255
        B[i][j] = (Blue + m) * 255

R = R.astype('uint8')
G = G.astype('uint8')
B = B.astype('uint8')

BGR[..., 0] = B
BGR[..., 1] = G
BGR[..., 2] = R

cv.imshow('RGB Formula', BGR)

cv.waitKey(0)
cv.destroyAllWindows()