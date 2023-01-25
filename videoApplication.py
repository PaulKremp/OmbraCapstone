from tkinter import *
import customtkinter as ct
import cv2
from PIL import Image
from PIL import ImageTk

##
## 'root' objects go first in this order to create the basis of the window before any buttons can be added
##

root = ct.CTk() # Creates Tkinter Window
root.geometry("200x200") # Changes default window size
root.title('Live Camera View') # Changes window heading title

ct.set_appearance_mode("dark") # Sets window appearance to dark mode
ct.set_default_color_theme("dark-blue") # Sets theme appearance to dark blue

cap = cv2.VideoCapture(0) # Capture video feed

if not cap.isOpened(): # Checks to make sure camera is accessible
    print("Camera Feed Unavailable")
    exit()

cap_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH) # Finds the pixel width of the capture
cap_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT) # Finds the pixel height of the capture

# class Video_Capture:
#     def __init__(self, video_source=0)
#         self.vid = cv2.VideoCapture(video_source)
#         if not self.vid.isOpened():
#             print("Camera Feed Unavailable")
#             exit()

#         cap_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH) # Finds the pixel width of the capture
#         cap_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT) # Finds the pixel height of the capture

#     def __del__(self):
#         if self.vid.isOpened():
#             self.vid.release()
#         self.window.mainloop()

#     def get_frame(self):
#         if self.vid.isOpened():
#             ret, frame = self.vid.read()
#             if ret:
#                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
#             else:
#                 return (ret, None)
#         else:
#             return (ret, None)

# class App:
#     def __init__(self, window, window_title, video_source=0):
#         self.window = window
#         self.window.title = 

while True:

    ret, videoInput = cap.read() # Reads the camera input

    if not ret: # Checks to make sure the video is able to be read
        print("Cannot access video")
        break

    videoRGB = cv2.cvtColor(videoInput, cv2.COLOR_BGR2RGB) # Change video feed from BGR to RGB Format
    videoPIL = Image.fromarray(videoInput) # Change video feed from RGB to PIL Format
    videoTK = ImageTk.PhotoImage(videoPIL) # Change video feed from PIL to Tkinter Format



    root.mainloop()
    Image = ct.CTkImage(light_image = None, dark_image = videoPIL, size = (200,200))

    

    





