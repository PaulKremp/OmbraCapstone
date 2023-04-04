import tkinter as tk
import customtkinter as ct
import cv2
import queue
import os
import shutil
from PIL import Image
from PIL import ImageTk
from FacialRecognition.utils import Recognizer 
from FacialRecognition.utils import EmbeddingGen
from FacialRecognition.utils import FaceDetect 

class Video_Capture:
    def __init__(self, video_source):
        self.vid = cv2.VideoCapture(video_source) # Takes in the video source as a variable
        recognizerBackend = "VGG-Face"
        faceDetectorBackend = "opencv"
        self.embeddings = EmbeddingGen("./db", recognizerBackend).outputEmbeddings(faceDetectorBackend)
        self.faceDetector = FaceDetect(faceDetectorBackend)
        self.faceRecognizer = Recognizer(recognizerBackend, self.embeddings, faceDetectorBackend)
        self.Q = queue.Queue()
        if not self.vid.isOpened(): # Checks if the video feed is available
            print("Camera Feed Unavailable")
            exit()       

    def get_frame(self): 

         # Create directories for recognizedFaces and unrecognizedFaces
        if not os.path.exists("captureImages/recognizedFaces"):
            os.makedirs("captureImages/recognizedFaces")
        if not os.path.exists("captureImages/unrecognizedFaces"):
            os.makedirs("captureImages/unrecognizedFaces")
        

        if self.vid.isOpened(): # Checks if video feed is accessible
            ret, frame = self.vid.read() # Takes a snapshot of each frame from the live feed
            self.Q.put(frame)   #Add Queue to combat buffer
            while self.Q.qsize() > 1:
                self.Q.get()
            recentFrame = self.Q.get()
            faces = self.faceDetector.detectFaces(recentFrame)
            captureImageWithBoxes = self.faceRecognizer.displayRecognizedFaceswithBoundingBoxes(faces, 0.2, recentFrame)
    
            if ret:
                # Returns the frame with the bounding boxes around the faces and the RGB Format of the frame
                return (ret, cv2.cvtColor(captureImageWithBoxes, cv2.COLOR_BGR2RGB))

class App():
    def __init__(self, video_source):
        self.window = ct.CTk()
        self.window.title("Live Camera Feed")
        self.window.appearance = ct.set_appearance_mode("dark")

        self.vid = Video_Capture(video_source)

        self.canvas = ct.CTkCanvas(self.window, width = 1280, height = 720, bg = 'black', highlightthickness = 0)
        self.canvas.pack(side=ct.LEFT)

        self.delay = 17
        self.update()

        self.settings_button = ct.CTkButton(self.window, fg_color = "#FF2400", hover_color = "#BA1B01", text_color = "#B4B4B4", width = 125, height = 125, text = "Settings", command = self.openSettings).pack(side = ct.TOP, padx = 5, pady = 2)
        self.screenshot_button = ct.CTkButton(self.window, fg_color = "#FF2400", hover_color = "#BA1B01", text_color = "#B4B4B4", width = 125, height = 125, text = "Screenshot", command = self.takeScreenshot).pack(side = ct.BOTTOM, padx = 5, pady = 2)
        self.window.mainloop()

    def update(self):
        ret, frame = self.vid.get_frame() # Snapshots the current frame from the camera feed

        if ret:
            frame = Image.fromarray(frame).resize((1280,720)) # Resizes image frame to 720p by default
            self.photo = ImageTk.PhotoImage(image = frame) # Converts this frame from RGB to CTk Format
            self.canvas.create_image(0, 0, image = self.photo, anchor = ct.NW) # Adds the image to the canvas
    
        self.window.after(self.delay, self.update) # Updates the image every 'self.delay' ms

    def takeScreenshot(self):
        print("Screenshot")

    def openSettings(self):
        settingsWindow = ct.CTkToplevel(self.window)
        settingsWindow.geometry('300x200')
        settingsWindow.title("Settings")

        self.backend_choice = ct.StringVar(value='Choose a Backend') # Sets an initial value for the dropdown menu
        self.backend_dropdown = ct.CTkOptionMenu(master = settingsWindow, fg_color = "#FF2400", dropdown_fg_color = "#FF2400", dropdown_hover_color = "#BA1B01", text_color = "#B4B4B4", dropdown_text_color = "#B4B4B4", button_hover_color = "#BA1B01", button_color = "#BA1B01", values = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface', 'mediapipe'], variable = self.backend_choice) # Creates choices for the dropdown menu
        self.backend_dropdown.pack(side = ct.TOP, padx = 5, pady = 20) # Places the dropdown at a location within the window

        self.model_choice = ct.StringVar(value='Choose a Model') # Sets an initial value for the dropdown menu
        self.model_dropdown = ct.CTkOptionMenu(master = settingsWindow, fg_color = "#FF2400", dropdown_fg_color = "#FF2400", dropdown_hover_color = "#BA1B01", text_color = "#B4B4B4", dropdown_text_color = "#B4B4B4", button_hover_color = "#BA1B01", button_color = "#BA1B01", values = ['VGG-Face', 'Facenet', 'Facenet512', 'OpenFace', 'DeepFace', 'DeepID', 'ArcFace', 'Dlib', 'SFace'], variable = self.model_choice) # Creates choices for the dropdown menu
        self.model_dropdown.pack(side=ct.TOP, pady=10) # Places the dropdown at a location within the window

        settingsWindow.mainloop()
         
videoSource = 0
#videoSource = 'rtsp://admin:sLUx5%23!!@192.168.40.42:554/cam/realmonitor?channel=1&subtype=0'
App(videoSource)
