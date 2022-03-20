#!python3
from time import sleep
import click
import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)


detector = HandDetector(detectionCon=0.8)
keys = [["Q","W","E","R","T","Y","U","I","O","P"],
         ["A","S","D","F","G","H","J","K","L"],
         ["Z","X","C","V","B","N","M",";","."]]
finalText = ""
clicked = False

def draw_all(img, button_list):
    
    for button in button_list:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, button.pos , (x+w,y+h),(0,0,255), cv2.FILLED)
        cv2.putText(img, button.text,(x+5,y+25), 
                        cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 3)

    return img

class Button():
    def __init__(self, pos, text, size=[40,40]) -> None:
        self.pos = pos
        self.text = text
        self.size = size
        
        

buttonList = []
for i in range(len(keys)): 
        for j,key in enumerate(keys[i]):
            buttonList.append(Button([60*j+30,60*i+30], key))

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bboxInfo = detector.findPosition(img)
    img = draw_all(img, buttonList)
    
    if lmList:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            if x < lmList[8][0] < x+w and y < lmList[8][1] < y +h:
                cv2.rectangle(img, button.pos , (x+w,y+h),(0,0,175), cv2.FILLED)
                cv2.putText(img, button.text,(x+5,y+25), 
                        cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 3)

                l,_,_ = detector.findDistance(8,12, img, draw=False)


                if l <= 50 and not clicked:
                    clicked = True
                    cv2.rectangle(img, button.pos , (x+w,y+h),(0,255,0), cv2.FILLED)
                    cv2.putText(img, button.text,(x+5,y+25), 
                            cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 3)
                    finalText += button.text
                if l > 60:
                    clicked = False
                    
    
    cv2.rectangle(img, (50,250) , (600, 450),(100,100,255), cv2.FILLED)
    cv2.putText(img, finalText,(60,425), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
