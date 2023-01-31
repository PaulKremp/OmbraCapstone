import cv2

# Opens the Video file
cap= cv2.VideoCapture('/home/paulk495/Videos/PeterRecording.mp4')  #Insert file name of video
i=0
counter = 0
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == False:
        break
    if counter != 0:
        if counter == 9:
            counter = 0
        else:
            counter +=1
        continue
    counter +=1
    # Load the cascade
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')   #make sure XML files download
    # Read the input image
    _, img = cap.read()
    # Convert into grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Display the output
    cv2.imshow('img', img)
    cv2.waitKey()
    if len(faces) > 0  :
        cv2.imwrite('Peter '+str(i)+'.jpg',frame)   #input title of person in the pictures
        i+=1

cap.release()
cv2.destroyAllWindows()
