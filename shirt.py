import os

import cvzone
import cv2
from cvzone.PoseModule import PoseDetector

cap = cv2.VideoCapture(0)
detector = PoseDetector()

shirtFolderPath = "Resources/Shirts"
listShirts = os.listdir(shirtFolderPath)
# Filter to only include image files
listShirts = [f for f in listShirts if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
listShirts.sort()
print(f"Shirts found: {listShirts}")
fixedRatio = 262 / 190  
shirtRatioHeightWidth = 581 / 440
imageNumber = 0
frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(f"Camera resolution: {frameWidth}x{frameHeight}")
imgButtonRight = cv2.imread("Resources/button.png", cv2.IMREAD_UNCHANGED)
imgButtonLeft = cv2.flip(imgButtonRight, 1)
counterRight = 0
counterLeft = 0
selectionSpeed = 10

while True:
    success, img = cap.read()
    img = detector.findPose(img)
    # img = cv2.flip(img,1)
    lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False)
    if lmList:
        # center = bboxInfo["center"]
        # lmList format: [id, x, y, z] - we need indices 0,1,2 for proper access
        # Landmark 11 = left shoulder, 12 = right shoulder
        lm11 = lmList[11][0:2]  # [x, y] for left shoulder
        lm12 = lmList[12][0:2]  # [x, y] for right shoulder
        imgShirt = cv2.imread(os.path.join(shirtFolderPath, listShirts[imageNumber]), cv2.IMREAD_UNCHANGED)
        print(f"Loading shirt: {listShirts[imageNumber]}")
        
        if imgShirt is not None:
            widthOfShirt = int(abs(lm11[0] - lm12[0]) * fixedRatio)
            heightOfShirt = int(widthOfShirt * shirtRatioHeightWidth)
            print(f"Coordinates - lm11: {lm11}, lm12: {lm12}, width: {widthOfShirt}, height: {heightOfShirt}")
            if widthOfShirt > 0 and heightOfShirt > 0:
                imgShirt = cv2.resize(imgShirt, (widthOfShirt, heightOfShirt))
                currentScale = abs(lm11[0] - lm12[0]) / 190
                offset = int(44 * currentScale), int(48 * currentScale)
                posX = int(lm12[0] - offset[0])
                posY = int(lm12[1] - offset[1])
                print(f"Overlay position: ({posX}, {posY}), offset: {offset}")

                try:
                    img = cvzone.overlayPNG(img, imgShirt, (posX, posY))
                    print("Overlay successful!")
                except Exception as e:
                    print(f"Error overlaying shirt: {e}")
        else:
            print(f"Failed to load shirt: {os.path.join(shirtFolderPath, listShirts[imageNumber])}")

        img = cvzone.overlayPNG(img, imgButtonRight, (1074, 293))
        img = cvzone.overlayPNG(img, imgButtonLeft, (72, 293))

        if lmList[16][1] < frameHeight // 3:  # Right wrist up
            counterRight += 1
            cv2.ellipse(img, (frameWidth // 2, frameHeight // 2), (66, 66), 0, 0,
                        counterRight * selectionSpeed, (0, 255, 0), 20)
            if counterRight * selectionSpeed > 360:
                counterRight = 0
                if imageNumber < len(listShirts) - 1:
                    imageNumber += 1
                    print(f"Selected shirt: {imageNumber} - {listShirts[imageNumber]}")
        elif lmList[15][1] < frameHeight // 3:  # Left wrist up
            counterLeft += 1
            cv2.ellipse(img, (frameWidth // 2, frameHeight // 2), (66, 66), 0, 0,
                        counterLeft * selectionSpeed, (0, 255, 0), 20)
            if counterLeft * selectionSpeed > 360:
                counterLeft = 0
                if imageNumber > 0:
                    imageNumber -= 1
                    print(f"Selected shirt: {imageNumber} - {listShirts[imageNumber]}")

        else:
            counterRight = 0
            counterLeft = 0

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('q') or key == 27:  # q or ESC to quit
        break