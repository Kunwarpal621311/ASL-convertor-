import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import  math
import time
from tkinter import messagebox
import tkinter as tk
import pyttsx3
from twilio.rest import Client
imgB = cv2.imread("Resources/background_asl2.jpg")
img_first = cv2.imread("Resources/front_page.jpg")

number =" "
def sendMassage(str):
    account_sid = 'AC6f397c3257c9dd5c34ed4245ac84ec54'
    auth_token = '598540e67de1b64cd215d40c2965bee5'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_='+13184968824',
        body=str,
        to="+91"+phone_number
    )

    # print(message.sid)



phone_number = " "
def submit():
    global phone_number
    phone_number = entry_phone_number.get()
    window.destroy()
window = tk.Tk()
window.title("Enter Phone Number")


window.geometry("300x150")

label_phone_number = tk.Label(window, text="Phone Number:")

entry_phone_number = tk.Entry(window)

button_submit = tk.Button(window, text="Submit", command=submit)

label_phone_number.pack()
entry_phone_number.pack()
button_submit.pack()

window.mainloop()



def TextToSpeech(text):
    # Initialize the pyttsx3 engine
    engine = pyttsx3.init()

    # Set voice properties
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Use the second voice in the list
    engine.setProperty('rate', 150)  # Speech rate (words per minute)
    engine.setProperty('volume', 1)  # Volume level (0 to 1)

    # Convert text to speech
    engine.say(text)
    engine.runAndWait()
def ask_permission():
    answer = messagebox.askyesno("Permission", "Allow to access the camera")
    if answer:
        # Perform action if user gives permission
        return True
    else:
        # Perform action if user does not give permission
        return False

def first_page():

    cv2.imshow("sign language converter ", img_first)
    cv2.setMouseCallback('sign language converter ', click_mouse_first)
    cv2.waitKey(0)


# confirmation button
# text =" "

# this function for mouse

def click_mouse_first(event, x, y, flag, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            # start
            if x >= 390 and x <= 889 and y >= 273 and y <= 323:
                start()
            # learn
            elif x >= 391 and x <= 889 and y >= 362 and y <= 413:
                lerning = cv2.VideoCapture("Resources/A (1280 × 720 px) (1).mp4")
                # imgFandQ = cv2.imread("Resources/fAndQ.jpg")
                while True:
                    res, frame = lerning.read()
                    cv2.imshow("Learn", frame)
                    k=cv2.waitKey(30)
                    if k== 27:
                        break
            # about
            elif x >= 391 and x <= 889 and y >= 362 and y <= 500:
                imgAbout = cv2.imread("Resources/aboutUs.jpg")
                cv2.imshow("ABOUT US ", imgAbout)
                cv2.waitKey(0)

            elif x >= 391 and x <= 899 and y >= 529 and y <= 585:
               exit(0)
            else:
                pass

#  video capture
Classifier = Classifier("Model/keras_model.h5")
def start():
    if ask_permission():
         cap = cv2.VideoCapture(0)
    else:
        pass
    # cap.set(3,1280)
    # cap.set(4,1024)
    Detector = HandDetector(maxHands=1)
    offSet = 20
    imgSize = 300
    # ML model for the program
    str = " "
    xt = 698
    yt = 250
    x_inc = 0
    # file = open("Text.txt", "w")
    # folder ="DATA/C"
    labels = ["A", "B", "C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    # labels =['A', 'B', 'C']

#  main loop start

    # cv2.destroyAllWindows()
    # cv2.destroyWindow("sign language converter" )
    # str = " "
    while True:
        res, img = cap.read()
        imgOutput = img.copy()

        hands, img = Detector.findHands(img)

        if hands:
            hand = hands[0]
            x, y, w, h = hand['bbox']
            if w == 0 or h == 0:
                continue
            # print('x= {} y ={} w ={} h ={}'.format(x,y,w,h))

            imgWhite = np.ones((imgSize, imgSize, 3), np.uint8)*255

            imgCrop = img[y-offSet :y+h+offSet , x-offSet: x+offSet+w]
            if imgCrop.size == 0:
                continue
            imgCropShape = imgCrop.shape


            assectRatio = h/w
            if w != 0 and h != 0:

                if assectRatio > 1:
                    k = imgSize/h
                    wCal = math.ceil(k*w)
                    imgResize = cv2.resize(imgCrop, (wCal,imgSize))
                    if imgResize.size == 0:
                        continue
                    imgResizeShape =imgResize.shape
                    wGap = math.ceil((imgSize-wCal)/2)
                    imgWhite[:, wGap:wCal+wGap] = imgResize
                    prediction, index = Classifier.getPrediction(imgWhite, draw= False)

                else:
                    k = imgSize / w
                    hCal = math.ceil(k * h)
                    imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                    if imgResize.size == 0:
                        continue
                    imgResizeShape = imgResize.shape
                    hGap = math.ceil((imgSize - hCal) / 2)
                    imgWhite[hGap:hCal + hGap, : ] = imgResize
                    prediction, index = Classifier.getPrediction(imgWhite, draw= False)

            cv2.putText(imgOutput, labels[index], (x, y-30), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 2)
            cv2.rectangle(imgOutput, (x-offSet,y- offSet), (x + w+offSet, y+ h+offSet), (255,0,255), 4)


        # cv2.imshow('camera', imgOutput)
        imgB[190:190 + 480, 39:39 + 640] = imgOutput

        cv2.imshow("Background", imgB)

        # cv2.imshow('image', imgB)
        # cv2.setMouseCallback("Background", click_mouse)


        k = cv2.waitKey(1)

        if k == 27:
             break
        elif k == ord('s') or k == ("S"):
            str += labels[index]
            # file.write(labels[index])
            if x_inc < 560:
                cv2.putText(imgB, labels[index], (xt+x_inc, yt), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 1)
                x_inc += 20
            else:
                yt += 25
                x_inc = 0
                cv2.putText(imgB, labels[index], (xt + x_inc, yt), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 1)
                x_inc += 20
        elif k == 32:
            str += " "
            # file.write(" ")
            if x_inc < 560:
                cv2.putText(imgB, " ", (x+x_inc, y), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0), 2)
                x_inc += 20
            else:
                yt += 25
                x_inc = 0
                cv2.putText(imgB, " ", (xt + x_inc, yt), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 1)
                x_inc += 20
        elif k == ord('p') or k == ord('P'):
            sendMassage(str)
            TextToSpeech(str)



first_page()

# print(str)

cv2.destroyAllWindows()
