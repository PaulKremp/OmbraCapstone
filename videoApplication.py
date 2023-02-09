from tkinter import *
import customtkinter as ct
import cv2
from PIL import Image
from PIL import ImageTk

class Video_Capture:
    def __init__(self, video_source):
        self.vid = cv2.VideoCapture(video_source) # Takes in the video source as a variable
        if not self.vid.isOpened(): # Checks if the video feed is available
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
        self.window = window # Creates CTk Root Window
        self.window.title(window_title) # Adds a title to the top of the window
        self.video_source = video_source # Sets video source variable
        self.window.appearance = ct.set_appearance_mode('dark') # Sets appearance of window to dark mode
        
        self.vid = Video_Capture(video_source) # Open Video Source

        self.canvas = ct.CTkCanvas(window, width = self.vid.width, height = self.vid.height) # Creates a canvas based on the dimensions of the image
        self.canvas.pack(side=ct.LEFT) 

        self.delay = 17 # Sets delay to 17ms (nearly 60 Frames Per Second)
        self.update()

        self.menus() # Creates the option menus

        self.window.mainloop() # Starts the CTk Window

    def menus(self):
        self.backend_choice = ct.StringVar(value='Choose a Backend')
        self.window.backend_dropdown = ct.CTkOptionMenu(master = self.window, values = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface', 'mediapipe'], variable = self.backend_choice)
        self.window.backend_dropdown.pack(side=ct.TOP, padx=5, pady=20)

        self.model_choice = ct.StringVar(value='Choose a Model')
        self.window.model_dropdown = ct.CTkOptionMenu(master = self.window, values = ['VGG-Face', 'Facenet', 'Facenet512', 'OpenFace', 'DeepFace', 'DeepID', 'ArcFace', 'Dlib', 'SFace'], variable = self.model_choice)
        self.window.model_dropdown.pack(side=ct.TOP, pady=10)

    def update(self):
        ret, frame = self.vid.get_frame() # Snapshots the current frame from the camera feed

        if ret:
            self.photo = ImageTk.PhotoImage(image = Image.fromarray(frame)) # Converts this frame from RGB to CTk Format
            self.canvas.create_image(0, 0, image = self.photo, anchor = ct.NW) # Adds the image to the canvas

        self.window.after(self.delay, self.update) # Updates the image every 'self.delay' ms

videoSource = 'rtsp://admin:sLUx5%23!!@192.168.40.42:554/cam/realmonitor?channel=1&subtype=00&authbasic=YWRtaW46c0xVeDUlMjMhIQ=='
App(ct.CTk(), 'Live Camera Feed', videoSource)



    





