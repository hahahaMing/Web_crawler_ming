import os
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image
import functools
import json
##TODO: git 有一段把pdf传上去了，学习如何修改一下让他不传，注意不要丢代码
pdfmetrics.registerFont(TTFont('Heiti', 'SimHei.ttf'))  #注册字体

INPUT_FOLDER = r'D:\SelfStudy\Git\mldnNoWatermask'
OUTPUT_FILE = r'D:\SelfStudy\Git\mldnNoWatermark.pdf'
titleDict = {}
with open(r'asset\c06\Titles.json','r')as f:
    titleDict = json.load(f)

folders = os.listdir(INPUT_FOLDER)

def cmpFolder(a,b):
    return int(a)-int(b)
    # return int(a.split("课时")[1].split("【")[0])-int(b.split("课时")[1].split("【")[0])

folders.sort(key=functools.cmp_to_key(cmpFolder))

c = canvas.Canvas(OUTPUT_FILE)
c.setPageSize((1839,2599))
chapterNum = 1
for folder in folders:
    pngs = os.listdir(os.path.join(INPUT_FOLDER, folder))
    chapterName = titleDict[folder]
    # 想把文件夹信息创建一页pdf
    c.setFont('Heiti', 50)
    c.drawRightString(1839-200, 1300, text=chapterName)
    c.bookmarkPage(str(chapterNum))
    c.addOutlineEntry(chapterName, str(chapterNum))
    c.bookmarkPage(str(chapterNum))
    c.showPage()
    chapterNum+=1
    for png in pngs:
        if os.path.getsize(os.path.join(INPUT_FOLDER, folder, png)) < 4000:
            continue
        pngPath = os.path.join(INPUT_FOLDER, folder, png)
        print(pngPath)
        # (w, h) = Image.open(pngPath).size
        # print(w, h)
        ## png 2 pdf
        c.drawImage(pngPath, 0, 0)
        c.showPage()
print("正在生成pdf。。。")
c.save()
