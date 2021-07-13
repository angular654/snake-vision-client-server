import cv2
import time
import zmq
import base64
import numpy as np
import HandTracking as htm
import ctypes 
from ordered_set import OrderedSet

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.bind('tcp://*:7777')
socket.setsockopt_string(zmq.SUBSCRIBE, np.compat.unicode(''))


overlayList = []

print(len(overlayList))
pTime = 0

detector = htm.handDetector(detectionCon=0.85)

tipIds = [4, 8, 12, 16, 20]

gestures = {
        'fist': 0,
        'hello': 0,
        'ok': 0,
        'rock': 0,
        'like': 0

}
filteredGestures = OrderedSet()

while True:
    image_string = socket.recv_string()
    raw_image = base64.b64decode(image_string)
    image = np.frombuffer(raw_image, dtype=np.uint8)
    frame = np.array(cv2.imdecode(image, 1))
    img = detector.findHands(frame)
    lmList = detector.findPosition(img, draw=False)
    # print(lmList)

    if len(lmList) != 0:
        fingers = []

        # Thumb
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # 4 Fingers
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        totalFingers = fingers.count(1)
        if(totalFingers == 0):
            gestures['fist'] += 1
            if gestures['fist'] >= 50:
                filteredGestures.add('fist')
        if(totalFingers == 5):
            gestures['hello'] += 1
            if gestures['hello'] >= 50:
                filteredGestures.add('hello')
        if (fingers == [1, 0, 1, 1, 1]):
            gestures['ok'] += 1
            if gestures['ok'] >= 50:
                filteredGestures.add('ok')
        if (fingers == [1, 1, 0, 0, 1] or fingers == [0, 1, 0, 0, 1]):
            gestures['rock'] += 1
            if gestures['rock'] >= 50:
                filteredGestures.add('rock')
        if(fingers == [0, 0, 0, 1, 1] or fingers == [0, 0, 1, 1, 1]):
            gestures['like'] += 1
            if gestures['like'] >= 50:
                filteredGestures.add('like')

    # filteredGestures = list(filter(lambda gesture: gestures[gesture] > 50, gestures))
    print(filteredGestures)

    if filteredGestures == {'like', 'fist', 'hello'}:
        ctypes.windll.user32.MessageBoxW(0, "Лампочка гори!", "Действие", 1)
        exit()

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.imshow("Image", img)
    cv2.waitKey(1)

