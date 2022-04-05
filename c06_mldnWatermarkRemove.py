import cv2
import os
import time
import numpy as np
import functools
import json
testImgPath = r'asset\c06\4.png'
testOutputPath = r'asset\c06\new.png'
watermarkImgPath = r'asset\c06\watermark.png'
onlyWatermarkPath = r'asset\c06\onlyWatermark.png'

INPUT_FOLDER = r'D:\SelfStudy\Git\mldn'
OUTPUT_FOLDER = r'D:\SelfStudy\Git\mldnNoWatermask'

if not os.path.exists(OUTPUT_FOLDER):
    os.mkdir(OUTPUT_FOLDER)
'''
1. 缩小水印范围

2. 遍历该区域如果像素差距很小就变为0，否则认为水印与正文重叠，暂时不变色

'''
## 改文件名为英文

# folders = os.listdir(INPUT_FOLDER)


# def cmpFolder(a, b):
#     return int(a.split("课时")[1].split("【")[0]) - int(
#         b.split("课时")[1].split("【")[0])


# folders.sort(key=functools.cmp_to_key(cmpFolder))

# chapterDict = {}
# chapterNum = 1

# for folder in folders:
#     # rename folder
#     os.rename(os.path.join(INPUT_FOLDER, folder),
#               os.path.join(INPUT_FOLDER, str(chapterNum)))
#     chapterDict[chapterNum] = folder
#     chapterNum += 1

# # create one dict file
# jsonStr = json.dumps(chapterDict)
# with open(os.path.join(INPUT_FOLDER,"chapterName.json",'w'))as f:
#     f.write(jsonStr)


## Watermark remove
watermark = cv2.imread(onlyWatermarkPath)

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

        img = cv2.imread(path)
        start = time.time()
        for x in range(1337, 1741):
            for y in range(1248, 1716):
                err = 0
                for channel in range(3):
                    err += pow(
                        watermark.item(x, y, channel) -
                        img.item(x, y, channel), 2)
                if err < 1000:
                    img.itemset((x, y, 0), 255)
                    img.itemset((x, y, 1), 255)
                    img.itemset((x, y, 2), 255)
        end = time.time()
        print(str(end - start) + 's')

        cv2.imwrite(os.path.join(subOutputFolderPath, imgPath), img)
        print(path)