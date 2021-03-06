import cv2
import numpy as np
import time
import os
import handTrackingModule as htm
import tesser as tes

#######################
brushThickness = 10
eraserThickness = 100
########################


folderPath = "Header"
myList = os.listdir(folderPath)
print(myList)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
print(len(overlayList))
header = overlayList[0]
drawColor = (0,17,255)

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 1080)

detector = htm.handDetector(detectionCon=0.65,maxHands=1)
xp, yp = 0, 0
imgCanvas = np.zeros((1080, 1280, 3), np.uint8)

while True:

    # 1. Import image
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # 2. Find Hand Landmarks
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        fingers = detector.fingersUp()
        # print(lmList)
        x1, y1 = lmList[8][1:]
        # tip of index and middle fingers
        if((fingers[1] == True and fingers[2] == False and fingers[3] == False and fingers[4] == False)):
            x1, y1 = lmList[8][1:]
        if ((fingers[1] == False and fingers[2] == True and fingers[3] == False and fingers[4] == False)):
            x1,y1=lmList[12][1:]
        if((fingers[1] == False and fingers[2] == False and fingers[3] == True and fingers[4] == False)):
            x1, y1 = lmList[16][1:]
        if((fingers[1] == False and fingers[2] == False and fingers[3] == False and fingers[4] == True)):
            x1, y1 = lmList[20][1:]


        x2, y2 = lmList[12][1:]

        # 3. Check which fingers are up

        # print(fingers)

        # 4. If Selection Mode - Two finger are up
        if ((fingers[1] and fingers[2]) or (fingers[2] and fingers[3]) or (fingers[3] and fingers[4])):
            xp, yp = 0, 0
            #print("Selection Mode")
            # # Checking for the click
            if y1 < 164:
                if 201 < x1 < 342:
                    header = overlayList[0]
                    drawColor = (0,17,255)
                elif 417 < x1 < 558:
                    header = overlayList[1]
                    drawColor = (255,5,38)
                elif 617 < x1 < 758:
                    header = overlayList[2]
                    drawColor = (51, 188, 83)
                elif 847 < x1 < 961:
                    header = overlayList[3]
                    drawColor = (0, 0, 0)

            #cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)

        # 5. If Drawing Mode - Index finger is up
        if ((fingers[1] == False and fingers[2] == True and fingers[3] == False and fingers[4] == False) \
                or (fingers[1] == True and fingers[2] == False and fingers[3] == False and fingers[4] == False) \
                or (fingers[1] == False and fingers[2] == False and fingers[3] == True and fingers[4] == False) \
                or (fingers[1] == False and fingers[2] == False and fingers[3] == False and fingers[4] == True)):

            #cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            #print("Drawing Mode")
            if xp == 0 and yp == 0:
                xp, yp = x1, y1


            if drawColor == (0, 0, 0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)

            else:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)

            xp, yp = x1, y1


        # # Clear Canvas when all fingers are up
        # if fingers[1] and fingers[2] and fingers[3] and fingers[4] == False and fingers[0] == False:
        #     imgCanvas = np.zeros((720, 1280, 3), np.uint8)

    imgCanvas = cv2.resize(imgCanvas, (img.shape[1], img.shape[0]))
    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.resize(imgCanvas, (img.shape[1], img.shape[0]))
    #imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    #img = cv2.bitwise_and(img,imgInv)
    img = cv2.bitwise_or(img,imgCanvas)


    # Setting the header image
    img[0:164, 0:1280] = header
    imgCanvas[0:164, 0:1280] = header

    img = cv2.addWeighted(img,0.5,imgCanvas,0.5,0)
    cv2.imshow("Image", img)
    cv2.imshow("Canvas", imgCanvas)
    #cv2.imshow("Inv", imgInv)
    cv2.waitKey(1)
    if cv2.waitKey(1)& 0xFF==ord('d'):
        tes.scrnshot()
