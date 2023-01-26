from tkinter import *
import customtkinter as ct
import cv2
from PIL import Image
from PIL import ImageTk

class Video_Capture:
    def __init__(self, video_source):
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            print("Camera Feed Unavailable")
            exit()

        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH) # Finds the pixel width of the capture
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT) # Finds the pixel height of the capture

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
        self.window.mainloop()

    def get_frame(self):
        if self.vid.isOpened(): # Checks if video feed is accessible
            ret, frame = self.vid.read() # Takes a snapshot of each frame from the live feed
            if ret:
               return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)) # Returns the original frame and the RGB Format of the frame
            else:
                return (ret, None) 
        else:
            return (ret, None)

class App:
    def __init__(self, window, window_title, video_source):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        self.window.appearance = ct.set_appearance_mode('dark')

        self.vid = Video_Capture(video_source) # Open Video Source

        self.canvas = ct.CTkCanvas(window, width = self.vid.width, height = self.vid.height)
        self.canvas.pack()
        
        self.delay = 17
        self.update()

        self.window.mainloop()

    def update(self):
        ret, frame = self.vid.get_frame()

        if ret:
            self.photo = ImageTk.PhotoImage(image = Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = ct.NW)

        self.window.after(self.delay, self.update)

App(ct.CTk(), 'Live Camera Feed', 0)





    

    





