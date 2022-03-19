#!python3
import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)


detector = HandDetector(detectionCon=0.8)
keys = [["Q","W","E","R","T","Y","U","I","O","P"],
         ["A","S","D","F","G","H","J","K","L"],
         ["Z","X","C","V","B","N","M"]]


class Button():
    def __init__(self, pos, text, size=[85,85]) -> None:
        self.pos = pos
        self.text = text
        self.size = size
        x, y = self.pos
        w, h = self.size
        cv2.rectangle(img, self.pos , (x+w,y+h),(0,0,255))
        cv2.putText(img, self.text,(x+20,y+65), 
                    cv2.FONT_HERSHEY_PLAIN, 4, (255,255,255), 4)
        

buttonList = []




while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bboxInfo = detector.findPosition(img)

    for x,key in enumerate(keys[0]):
        buttonList.append(Button([100*x+50,50], key))
    
    


    cv2.imshow("Image", img)
    cv2.waitKey(1)
