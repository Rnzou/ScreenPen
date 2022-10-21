# _*_ coding : utf-8 _*_
# @time : 23:04 2022/10/6
# @author : wan
# @file : PROJECT1
# @project : opencv
import cv2
import numpy as np

cap = cv2.VideoCapture(1)

ColorHSV = [[0, 200, 109, 2, 245, 237],
            [113, 0, 9, 179, 137, 255]]
PenBGR = [[0, 0, 255],
          [255, 0, 0]]

drawPoints = []

def findPen(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    for i in range(len(ColorHSV)):
        lower = np.array(ColorHSV[i][:3])
        upper = np.array(ColorHSV[i][3:6])

        mask = cv2.inRange(hsv, lower, upper)
        result = cv2.bitwise_and(img, img, mask=mask)

        penx, peny = findContour(mask, i)
        cv2.circle(imgContours, (penx, peny), 10, PenBGR[i], cv2.FILLED)
        if penx != -1:
            drawPoints.append([penx, peny, i])

def draw(drawPoints):
    for point in drawPoints:
        cv2.circle(imgContours, (point[0], point[1]), 10, PenBGR[0], cv2.FILLED)

def findContour(img, i):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, z = -1, -1, -1, -1
    for cnt in contours:
        # cv2.drawContours(imgContours, cnt, -1, (255, 0, 0), 2)
        area = cv2.contourArea(cnt)
        if i==0:
            if area > 30:
                peri = cv2.arcLength(cnt, True)
                vertices = cv2.approxPolyDP(cnt, peri * 0.02, True)
                x, y, z, w = cv2.boundingRect(vertices)
        else:
            continue
            if area > 450:
                peri = cv2.arcLength(cnt, True)
                vertices = cv2.approxPolyDP(cnt, peri * 0.02, True)
                x, y, z, w = cv2.boundingRect(vertices)
    return x+z//2, y


while True:
    get, frame = cap.read()
    if get:
        imgContours = frame.copy()
        cv2.imshow('video', frame)
        findPen(frame)
        draw(drawPoints)
        cv2.imshow('imgContours', imgContours)
    else:
        break
    if cv2.waitKey(10) == ord('q'):
        break