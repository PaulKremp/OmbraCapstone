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
import datetime

class Video_Capture:
    def __init__(self, video_source):
        self.vid = cv2.VideoCapture(video_source) # Takes in the video source as a variable

        self.recognizerBackend = recognizerOptionGlobal
        self.faceDetectorBackend = backendOptionGlobal

        print("This is the model: " + self.recognizerBackend + " This is the backend: " + self.faceDetectorBackend)

        self.embeddings = EmbeddingGen("./db", self.recognizerBackend).outputEmbeddings(self.faceDetectorBackend)
        self.faceDetector = FaceDetect(self.faceDetectorBackend)
        self.faceRecognizer = Recognizer(self.recognizerBackend, self.embeddings, self.faceDetectorBackend)
        
        self.Q = queue.Queue()
        if not self.vid.isOpened(): # Checks if the video feed is available
            print("Camera Feed Unavailable")
            exit()       

    def get_faces(self, video_source):
        self.vid = cv2.VideoCapture(video_source) # Takes in the video source as a variable

        self.recognizerBackend = recognizerOptionGlobal
        self.faceDetectorBackend = backendOptionGlobal

        print("This is the model: " + self.recognizerBackend + " This is the backend: " + self.faceDetectorBackend)

        self.embeddings = EmbeddingGen("./db", self.recognizerBackend).outputEmbeddings(self.faceDetectorBackend)
        self.faceDetector = FaceDetect(self.faceDetectorBackend)
        self.faceRecognizer = Recognizer(self.recognizerBackend, self.embeddings, self.faceDetectorBackend)
        
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
        self.video_source = video_source
        self.recognizerOption = ct.StringVar(value = "VGG-Face")
        self.backendOption = ct.StringVar(value = "opencv")

        global recognizerOptionGlobal
        global backendOptionGlobal

        recognizerOptionGlobal = self.recognizerOption.get()
        backendOptionGlobal = self.backendOption.get()

        self.vid = Video_Capture(video_source)

        self.canvas = ct.CTkCanvas(self.window, width = 1280, height = 720, bg = 'black', highlightthickness = 0)
        self.canvas.pack(side=ct.LEFT)

        self.delay = 17
        self.update()

        self.settings_button = ct.CTkButton(self.window, fg_color = "#EA2100", hover_color = "#BA1B01", text_color = "#000000", width = 125, height = 125, text = "Settings", command = self.openSettings).pack(side = ct.TOP, padx = 5, pady = 2)
        self.screenshot_button = ct.CTkButton(self.window, fg_color = "#EA2100", hover_color = "#BA1B01", text_color = "#000000", width = 125, height = 125, text = "Screenshot", command = self.takeScreenshot).pack(side = ct.BOTTOM, padx = 5, pady = 2)
        
        self.window.mainloop()

    def update(self):
        ret, frame = self.vid.get_frame() # Snapshots the current frame from the camera feed

        if ret:
            frame = Image.fromarray(frame).resize((1280,720)) # Resizes image frame to 720p by default
            self.photo = ImageTk.PhotoImage(image = frame) # Converts this frame from RGB to CTk Format
            self.canvas.create_image(0, 0, image = self.photo, anchor = ct.NW) # Adds the image to the canvas
    
        self.window.after(self.delay, self.update) # Updates the image every 'self.delay' ms

    def takeScreenshot(self):
        ret, frame = self.vid.get_frame()
        directory_path = os.path.expanduser('~')
        image_path = f"{directory_path}/Pictures"
        timestamp = datetime.datetime.now().strftime("%m-%d-%Y, %H-%M-%S")
        if ret:
            frame = Image.fromarray(frame).resize((1280,720)).save(f"{image_path}/{timestamp}.jpg")

    def openSettings(self):
        self.settingsWindow = ct.CTkToplevel(self.window)
        self.settingsWindow.attributes("-topmost", True)
        self.settingsWindow.geometry('300x200')
        self.settingsWindow.title("Settings")

        self.backend_dropdown = ct.CTkOptionMenu(master = self.settingsWindow, fg_color = "#EA2100", dropdown_fg_color = "#EA2100", dropdown_hover_color = "#BA1B01", text_color = "#000000", dropdown_text_color = "#000000", button_hover_color = "#BA1B01", button_color = "#BA1B01", values = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface', 'mediapipe'], variable = self.backendOption) # Creates choices for the dropdown menu
        self.backend_dropdown.pack(side = ct.TOP, padx = 5, pady = 20) # Places the dropdown at a location within the window

        self.recognizer_dropdown = ct.CTkOptionMenu(master = self.settingsWindow, fg_color = "#EA2100", dropdown_fg_color = "#EA2100", dropdown_hover_color = "#BA1B01", text_color = "#000000", dropdown_text_color = "#000000", button_hover_color = "#BA1B01", button_color = "#BA1B01", values = ['VGG-Face', 'Facenet', 'Facenet512', 'OpenFace', 'DeepFace', 'DeepID', 'ArcFace', 'Dlib', 'SFace'], variable = self.recognizerOption) # Creates choices for the dropdown menu
        self.recognizer_dropdown.pack(side=ct.TOP, pady=10) # Places the dropdown at a location within the window

        self.confirm_button = ct.CTkButton(master = self.settingsWindow, fg_color = "#EA2100", hover_color = "#BA1B01", text_color = "#000000", width = 10, height = 10, text = "Confirm", command = self.updateSettings).pack(side = ct.BOTTOM, padx = 5, pady = 10)
        self.settingsWindow.mainloop()

    def updateSettings(self):
        global recognizerOptionGlobal
        global backendOptionGlobal

        recognizerOptionGlobal = self.recognizerOption.get()
        backendOptionGlobal = self.backendOption.get()

        self.settingsWindow.destroy()
        self.vid.get_faces(self.video_source)


videoSource = 0
#videoSource = 'rtsp://admin:sLUx5%23!!@192.168.40.42:554/cam/realmonitor?channel=1&subtype=0'
App(videoSource)
