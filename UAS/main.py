import cv2 as cv
import numpy as np

import requests

# URL = "http://192.168.245.130" #url esp
URL = "http://192.168.245.130"

video = cv.VideoCapture(URL + ":81/stream") #capture video stream from ESP

def set_resolution(url: str, index: int=1, verbose: bool=False) :
    try:
        if verbose:
            resolutions = "10: UXGA(1600x1200)\n9: SXGA(1280x1024)\n8: XGA(1024x768)\n7: SVGA(800x600)\n6: VGA(640x480)\n5: CIF(400x296)\n4: QVGA(320x240)\n3: HQVGA(240x176)\n0: QQVGA(160x120)"
            print("available resolutions\n{}".format(resolutions))

        if index in [10, 9, 8, 7, 6, 5, 4, 3, 0]:
            requests.get(url + "/control?var=framesize&val={}".format(index))
        else:
            print("Wrong index")
    except:
        print("SET_RESOLUTION: something went wrong")

def set_quality(url: str, value: int=1, verbose: bool=False) :
    try:
        if value >= 4 and value <=63:
            requests.get(url + "/control?var=quality&val={}".format(value))
    except:
        print("SET_QUALITY: something went wrong")

def set_awb(url: str, awb: int=1) :
    try:
        awb = not awb
        requests.get(url + "/control?var=awb&val={}".format(1 if awb else 0))
    except:
        print("SET_QUALITY: something went wrong")
    return awb

def nothing(x):
    pass

#create control slider
cv.namedWindow("control")

cv.createTrackbar("LH","control",0,255,nothing)
cv.createTrackbar("LS","control",0,255,nothing)
cv.createTrackbar("LV","control",0,255,nothing)

cv.createTrackbar("UH","control",255,255,nothing)
cv.createTrackbar("US","control",255,255,nothing)
cv.createTrackbar("UV","control",255,255,nothing)

if __name__ == '__main__' : 

    set_resolution(url=URL, index=8) #set video stream resolutions
    set_quality(url=URL, value=4)    #set video stream quality
    set_awb(url=URL, awb= 1)         #set video strean awb

    while True : #loop program

        if video.isOpened() :
            ret, frame = video.read()

            hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

            l_h = cv.getTrackbarPos("LH","control")
            l_s = cv.getTrackbarPos("LS","control")
            l_v = cv.getTrackbarPos("LV","control")

            u_h = cv.getTrackbarPos("LH","control")
            u_s = cv.getTrackbarPos("US","control")
            u_v = cv.getTrackbarPos("UV","control")

            l_b = np.array([l_h, l_s, l_v])
            u_b = np.array([u_h, u_s, u_v])

            mask = cv.inRange(hsv_frame,l_b,u_b)
            result = cv.bitwise_and(frame,frame,mask=mask)

            cv.imshow("source",frame)
            cv.imshow("mask",mask)
            cv.imshow("Result",result)

            if cv.waitKey(1) & 0xFF == ord('q'):
                break