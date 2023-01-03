# Import required Libraries
import datetime
import tkinter as tk
from PIL import Image, ImageTk
import cv2 as cv
from tkinter import filedialog
import numpy as np

import requests
# Create an instance of TKinter Window or frame
window = tk.Tk()

# Set the size of the window
x=1200
y=1000
window.geometry(f'{x}x{y}')

# Create a Label to capture the Video frames
label = tk.Label(text='GUI DETEKSI WARNA', font=('Times_New_Roman',30))
label.pack(side=tk.TOP)
frame0 = tk.LabelFrame(text='Penampil Video', font=('Times_New_Roman', 15))
frame0.pack()
frame = tk.LabelFrame(frame0,text='Kamera ESP32 CAM', font=('Times_New_Roman', 15))
frame.pack(side=tk.LEFT)
frame2 = tk.LabelFrame(frame0,text='Hasil Masking Citra', font=('Times_New_Roman', 15))
frame2.pack(side=tk.LEFT)
frame3 = tk.LabelFrame(frame0,text='Hasil Deteksi Warna', font=('Times_New_Roman', 15))
frame3.pack(side=tk.LEFT)

imageframe = tk.Label(frame, width=120, height=30)
imageframe.pack()
imageframe2 = tk.Label(frame2, width=120, height=30)
imageframe2.pack()
imageframe3 = tk.Label(frame3, width=120, height=30)
imageframe3.pack()

#create control slider
frameSlider = tk.LabelFrame(text='Indikator', font=('Times_New_Roman', 12))
frameSlider.pack()
frameLH = tk.LabelFrame(frameSlider,text='Nilai LH', font=('Times_New_Roman', 15))
frameLH.pack(side=tk.LEFT)
scale1 = tk.Scale(frameLH,from_=0,to=255,orient=tk.HORIZONTAL)
scale1.pack()

frameLS = tk.LabelFrame(frameSlider,text='Nilai LS', font=('Times_New_Roman', 15))
frameLS.pack(side=tk.LEFT)
scale2 = tk.Scale(frameLS,from_=0,to=255,orient=tk.HORIZONTAL)
scale2.pack()

frameLV = tk.LabelFrame(frameSlider,text='Nilai LV', font=('Times_New_Roman', 15))
frameLV.pack(side=tk.LEFT)
scale3 = tk.Scale(frameLV,from_=0,to=255,orient=tk.HORIZONTAL)
scale3.pack()

frameUH = tk.LabelFrame(frameSlider,text='Nilai UH', font=('Times_New_Roman', 15))
frameUH.pack(side=tk.LEFT)
scale4 = tk.Scale(frameUH,from_=255,to=255,orient=tk.HORIZONTAL)
scale4.pack()

frameUS = tk.LabelFrame(frameSlider,text='Nilai US', font=('Times_New_Roman', 15))
frameUS.pack(side=tk.LEFT)
scale5 = tk.Scale(frameUS,from_=255,to=255,orient=tk.HORIZONTAL)
scale5.pack()

frameUV = tk.LabelFrame(frameSlider,text='Nilai UV', font=('Times_New_Roman', 15))
frameUV.pack(side=tk.LEFT)
scale6 = tk.Scale(frameUV,from_=255,to=255,orient=tk.HORIZONTAL)
scale6.pack()

# URL = "http://192.168.43.252"
URL = "http://192.168.77.130"

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



if __name__ == '__main__' : 

    set_resolution(url=URL, index=8) #set video stream resolutions
    set_quality(url=URL, value=4)    #set video stream quality
    set_awb(url=URL, awb= 1)         #set video strean awb

# Define function to show frame.
def show_frames():
   # Get the latest frame and convert into Image
   ret, frame = video.read()
   frame1 = cv.cvtColor(frame,cv.COLOR_BGR2RGB)
   hsv_frame = cv.cvtColor(frame1, cv.COLOR_BGR2HSVFULL)
   l_h = int(scale1.get())
   l_s = int(scale2.get())
   l_v = int(scale3.get())
   u_h = int(scale4.get())
   u_s = int(scale5.get())
   u_v = int(scale6.get())
   l_b = np.array([l_h, l_s, l_v])
   u_b = np.array([u_h, u_s, u_v])  
   mask = cv.inRange(hsv_frame,l_b,u_b)
   result = cv.bitwise_and(frame1,frame1,mask=mask)
   
   img1 = Image.fromarray(frame1)
   img2 = Image.fromarray(mask)
   img3 = Image.fromarray(result)
   
   # Convert image to PhotoImage
   imgtk = ImageTk.PhotoImage(image = img1)
   imageframe.imgtk = imgtk
   imageframe.configure(image=imgtk, width=400, height=300)
   imgtk2 = ImageTk.PhotoImage(image=img2)
   imageframe2.imgtk = imgtk2
   imageframe2.configure(image=imgtk2, width=400, height=300)
   imgtk3 = ImageTk.PhotoImage(image=img3)
   imageframe3.imgtk = imgtk3
   imageframe3.configure(image=imgtk3, width=400, height=300)
   
   # Repeat after an interval to capture continiously
   imageframe.after(20, show_frames)

show_frames()
window.mainloop()