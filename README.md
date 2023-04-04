# OmbraCapstone
Ombra Capstone
This is the software stack for Group #9 Block O-Mbras capstone for the Fall 22' Semester

TO TEST VIDEOS IR 6 feet, IR 8 feet, and IR 10 feet: these tests are being conducted to determine if processing speed is an issue within loss of efficiency in IR facial recognition and detection. 

Videos are located in the baselineVideos folder. Please run tests on 6ftIR.mp4, 8ftIR.mp4 and 10ftIR.mp4. 

Everything needed is in the appication-dev branch. To run the main file, only use videoApplication.py. 

In line 119 of videoApplication.py, you will need to copy the relative path of each of the 3 videos to run without debugging for testing. All videos are located in the baselineVideos folder. 

The captureImages folder is where the videoApplication.py folder will store the captureImages generated while running each video. 

After the first video has ran through in its completion and all captureImages have been stored, please store these into a file and title it by what video is ran. This must be done each time because the captureImages folder will need "reset". You can simply delete the recognizedFaces and unrecognizedFaces subfolders within the captureImage folder, and once you compile the code again with the next IR video path, two new folders will be created on their own. You only need to store and delete the subfolders within captureImages each time you run a new video. 

The data for the capture images does not need analyzed by you, simply send us the 3 folders for the 3 IR videos with their captureImages folder and subfolders and we will count for the efficiency. 

Thank you!
