import cv2
import RainFilter

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
    #img = RainFilter.add_rain(img)
    # Convert into grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    #Consider adding rain filter here https://www.freecodecamp.org/news/image-augmentation-make-it-rain-make-it-snow-how-to-modify-a-photo-with-machine-learning-163c0cb3843f/
    #def generate_random_lines(imshape,slant,drop_length):    drops=[]    for i in range(1500): ## If You want heavy rain, try increasing this        if slant<0:            x= np.random.randint(slant,imshape[1])        else:            x= np.random.randint(0,imshape[1]-slant)        y= np.random.randint(0,imshape[0]-drop_length)        drops.append((x,y))    return drops            def add_rain(image):        imshape = image.shape    slant_extreme=10    slant= np.random.randint(-slant_extreme,slant_extreme)     drop_length=20    drop_width=2    drop_color=(200,200,200) ## a shade of gray    rain_drops= generate_random_lines(imshape,slant,drop_length)        for rain_drop in rain_drops:        cv2.line(image,(rain_drop[0],rain_drop[1]),(rain_drop[0]+slant,rain_drop[1]+drop_length),drop_color,drop_width)    image= cv2.blur(image,(7,7)) ## rainy view are blurry        brightness_coefficient = 0.7 ## rainy days are usually shady     image_HLS = cv2.cvtColor(image,cv2.COLOR_RGB2HLS) ## Conversion to HLS    image_HLS[:,:,1] = image_HLS[:,:,1]*brightness_coefficient ## scale pixel values down for channel 1(Lightness)    image_RGB = cv2.cvtColor(image_HLS,cv2.COLOR_HLS2RGB) ## Conversion to RGB    return image_RGB



    # Display the output
    cv2.imshow('img', img)
    cv2.waitKey()
    if len(faces) > 0  :
        cv2.imwrite('PeterRain '+str(i)+'.jpg',frame)   #input title of person in the pictures
        i+=1

cap.release()
cv2.destroyAllWindows()
