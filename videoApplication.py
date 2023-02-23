from tkinter import *
import customtkinter as ct
import cv2
import time
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
        if not self.vid.isOpened(): # Checks if the video feed is available
            print("Camera Feed Unavailable")
            exit()        
        #self.embeddings = EmbeddingGen("./db", recognizerBackend).refreshPKL(faceDetectorBackend)
        
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
        self.window.mainloop()
        

    def get_frame(self): 
        #imported from main.py backend (lines 29-37)
        recognizerBackend = "VGG-Face"
        faceDetectorBackend = "opencv"
       
        embeddings = EmbeddingGen(
        "./db", recognizerBackend).outputEmbeddings(faceDetectorBackend)
        faceDetector = FaceDetect(faceDetectorBackend)
        faceRecognizer = Recognizer(
        recognizerBackend, embeddings, faceDetectorBackend)

         # Create directories for recognizedFaces and unrecognizedFaces
        if not os.path.exists("captureImages/recognizedFaces"):
            os.makedirs("captureImages/recognizedFaces")
        if not os.path.exists("captureImages/unrecognizedFaces"):
            os.makedirs("captureImages/unrecognizedFaces")
        

        if self.vid.isOpened(): # Checks if video feed is accessible
            start_time = time.time()
            ret, frame = self.vid.read() # Takes a snapshot of each frame from the live feed
            faces = faceDetector.detectFaces(frame)
            keyPress = faceRecognizer.displayRecognizedFaces(faces, 0.2, frame)
            #captureImage = faceRecognizer.displayCaptureImageFace(faces, 0.2, frame)
            captureImageWithBoxes = faceRecognizer.displayRecognizedFaceswithBoundingBoxes(faces, 0.2, frame)
            
           

            if keyPress == ord("r"):
                # Delete contents of recognizedFaces and unrecognizedFaces directories
                shutil.rmtree("captureImages/recognizedFaces", ignore_errors=True)
                shutil.rmtree("captureImages/unrecognizedFaces", ignore_errors=True)

                # Create recognizedFaces and unrecognizedFaces directories
                os.makedirs("captureImages/recognizedFaces")
                os.makedirs("captureImages/unrecognizedFaces")
            if keyPress == ord("q"):
                cv2.destroyAllWindows()
                exit()
    
            if ret:
                # Returns the frame with the bounding boxes around the faces and the RGB Format of the frame
                return (ret, cv2.cvtColor(captureImageWithBoxes, cv2.COLOR_BGR2RGB)) 
          
        
            
            


class App:
    def __init__(self, window, window_title, video_source):
        self.window = window # Creates CTk Root Window
        self.window.title(window_title) # Adds a title to the top of the window
        self.video_source = video_source # Sets video source variable
        self.window.appearance = ct.set_appearance_mode('dark') # Sets appearance of window to dark mode
        
        self.vid = Video_Capture(video_source) # Open Video Source

        self.canvas = ct.CTkCanvas(window, width = 1280, height = 720, bg ='black', highlightthickness = 0) # Creates a canvas with dimensions of 720p for the camera
        self.canvas.pack(side=ct.LEFT) 

        self.delay = 17 # Sets delay to 17ms (nearly 60 Frames Per Second)
        self.update()

        self.screenshot() # Creates functional screenshot button

        #self.settings() 
        self.menus() # Creates the option menus

        self.window.mainloop() # Starts the CTk Window

    def menus(self):
        # self.settings_window = Toplevel(self.window)
        # self.settings_window.geometry("400x200")
        # self.settings_window.title('Settings')
        # self.settings_canvas = ct.CTkCanvas(self.settings_window, width = 400, height = 200, bg = 'black', highlightthickness = 0)
        self.backend_choice = ct.StringVar(value='Choose a Backend') # Sets an initial value for the dropdown menu
        self.window.backend_dropdown = ct.CTkOptionMenu(master = self.window, values = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface', 'mediapipe'], variable = self.backend_choice) # Creates choices for the dropdown menu
        self.window.backend_dropdown.pack(side = ct.TOP, padx = 5, pady = 20) # Places the dropdown at a location within the window

        self.model_choice = ct.StringVar(value='Choose a Model') # Sets an initial value for the dropdown menu
        self.window.model_dropdown = ct.CTkOptionMenu(master = self.window, values = ['VGG-Face', 'Facenet', 'Facenet512', 'OpenFace', 'DeepFace', 'DeepID', 'ArcFace', 'Dlib', 'SFace'], variable = self.model_choice) # Creates choices for the dropdown menu
        self.window.model_dropdown.pack(side=ct.TOP, pady=10) # Places the dropdown at a location within the window

    # def settings(self):
    #     self.settings_button = ct.CTkButton(master = self.window, width = 150, height = 150, text = 'Settings', command = self.menus()).pack(side = TOP, pady = 5)

    def update(self):
        ret, frame = self.vid.get_frame() # Snapshots the current frame from the camera feed

        if ret:
            start_time = time.time()
            frame = Image.fromarray(frame).resize((1280,720)) # Resizes image frame to 720p by default
            self.photo = ImageTk.PhotoImage(image = frame) # Converts this frame from RGB to CTk Format
            self.canvas.create_image(0, 0, image = self.photo, anchor = ct.NW) # Adds the image to the canvas
            print(f"fps: {1/(time.time() - start_time)}")

        self.window.after(self.delay, self.update) # Updates the image every 'self.delay' ms
        
    def screenshot(self):
        self.screenshot_button = ct.CTkButton(master = self.window, width=150, height=150, text='Snapshot').pack(side=ct.BOTTOM, padx=5) #command=self.screenshot_event

#videoSource = 0
videoSource = 'rtsp://admin:sLUx5%23!!@192.168.40.42:554/cam/realmonitor?channel=1&subtype=0'
App(ct.CTk(), 'Live Camera Feed', videoSource)



    





