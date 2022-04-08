import cv2
import numpy as np
import os
import time

testImgPath = r'asset\c06\4.png'
testOutputPath = r'asset\c06\new.png'

INPUT_FOLDER = r'D:\SelfStudy\Git\mldnNoWatermask'
OUTPUT_FOLDER = r'D:\SelfStudy\Git\mldnNoAD'

if not os.path.exists(OUTPUT_FOLDER):
    os.mkdir(OUTPUT_FOLDER)

for subFolder in os.listdir(INPUT_FOLDER):
    if '.' in subFolder:
        continue
    subOutputFolderPath = os.path.join(OUTPUT_FOLDER, subFolder)
    if not os.path.exists(subOutputFolderPath):
        os.mkdir(subOutputFolderPath)
    for imgPath in os.listdir(os.path.join(INPUT_FOLDER, subFolder)):
        path = os.path.join(INPUT_FOLDER, subFolder, imgPath)
        if os.path.getsize(path) < 4000:
            continue
        start = time.time()
        img = cv2.imread(path)

        img[124:259,128:1553] = 255
        img[43:276,1632:1802] = 255
        img[2411:2448,128:1556] = 255
        img[2370:2598,1645:1810] = 255

        cv2.imwrite(os.path.join(subOutputFolderPath, imgPath), img)
        
        print(path)
        end = time.time()
        print(str(end - start) + 's')

