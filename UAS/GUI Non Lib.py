# Import required Libraries
import tkinter as tk
from PIL import Image, ImageTk
import cv2 as cv
from tkinter import filedialog
import numpy as np


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
frame = tk.LabelFrame(frame0,text='Kamera ESPCAM', font=('Times_New_Roman', 15))
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
frameSlider = tk.LabelFrame(text='Slider', font=('Times_New_Roman', 12))
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
scale4 = tk.Scale(frameUH,from_=0,to=255,orient=tk.HORIZONTAL)
scale4.pack()

frameUS = tk.LabelFrame(frameSlider,text='Nilai US', font=('Times_New_Roman', 15))
frameUS.pack(side=tk.LEFT)
scale5 = tk.Scale(frameUS,from_=0,to=255,orient=tk.HORIZONTAL)
scale5.pack()

frameUV = tk.LabelFrame(frameSlider,text='Nilai UV', font=('Times_New_Roman', 15))
frameUV.pack(side=tk.LEFT)
scale6 = tk.Scale(frameUV,from_=0,to=255,orient=tk.HORIZONTAL)
scale6.pack()


video = cv.VideoCapture(0) #capture video stream from ESP


# Define function to show frame.
def show_frames():
   # Get the latest frame and convert into Image
   ret, frame = video.read()
   frame1 = cv.cvtColor(frame,cv.COLOR_BGR2RGB)
   #hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
   bgr = frame.astype('float')
   B = (bgr[:, :, 0])
   G = (bgr[:, :, 1])
   R = (bgr[:, :, 2])

   H = np.zeros([bgr.shape[0], bgr.shape[1]], dtype=float)
   S = np.zeros([bgr.shape[0], bgr.shape[1]], dtype=float)
   V = np.zeros([bgr.shape[0], bgr.shape[1]], dtype=float)
   HSV = np.zeros((bgr.shape[0], bgr.shape[1], 3), 'uint8')

   for i in range(bgr.shape[0]):
      for j in range(bgr.shape[1]):

         Bnorm = B[i][j] / float(255)  # normalisasi
         Gnorm = G[i][j] / float(255)
         Rnorm = R[i][j] / float(255)

         Cmax = max(Bnorm, Gnorm, Rnorm)  # nilai maksimum dari semua komponen warna
         Cmin = min(Bnorm, Gnorm, Rnorm)  # nilai minimum dari semua komponen warna
         delta = Cmax - Cmin

         # hitung H
         if (delta == 0):
            H[i][j] = 0
         elif (Rnorm == Cmax):
            H[i][j] = (60 * ((Gnorm - Bnorm) / delta) + 0 % 6)
         elif (Gnorm == Cmax):
            H[i][j] = (60 * ((Bnorm - Rnorm) / delta) + 2)
         elif (Bnorm == Cmax):
            H[i][j] = (60 * ((Rnorm - Gnorm) / delta) + 4)

         # hitung S
         if (Cmax == 0):
            S[i][j] = 0
         else:
            S[i][j] = (delta / Cmax) * 100

         # hitung V
         V[i][j] = Cmax * 100

   # menampilkan citra yang telah dibaca/import
   H = H.astype('uint8')
   S = S.astype('uint8')
   V = V.astype('uint8')
   HSV[..., 0] = H
   HSV[..., 1] = S
   HSV[..., 2] = V
   #hsv_frame= cv.cvtColor(video.read()[1],cv.COLOR_BGR2HSV)
   l_h = int(scale1.get())
   l_s = int(scale2.get())
   l_v = int(scale3.get())
   u_h = int(scale4.get())
   u_s = int(scale5.get())
   u_v = int(scale6.get())
   l_b = np.array([l_h, l_s, l_v])
   u_b = np.array([u_h, u_s, u_v])  
   mask = cv.inRange(HSV,l_b,u_b)
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