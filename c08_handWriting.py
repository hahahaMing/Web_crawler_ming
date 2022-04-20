## 15张图。。。还有规律可还行。。。
import functools
import requests
import os
from reportlab.pdfgen import canvas
# "https://book.yunzhan365.com/yyhg/ypqm/files/mobile/15.jpg"

WEB_HEAD = "https://book.yunzhan365.com/yyhg/ypqm/files/mobile/"

OUTPUT_FOLDER = "asset\\c08"
OUTPUT_FILE = r'D:\SelfStudy\Git\handwriting.pdf'
def download_img(imgurl,path):
    try:    
        rsp = requests.get(imgurl)
        if rsp.status_code == 200:
            content = rsp.content
            # 注意下面open里面的mode是"wb+", 因为content的类型是bytes
            with open(path, "wb+") as f:
                f.write(content)
            return str(content)
    except Exception:
        print ('load img err. err=',Exception)

# for x in range(15):
#     download_img(WEB_HEAD+str(x+1)+'.jpg',os.path.join(OUTPUT_FOLDER,str(x+1)+'.jpg'))

## pdf

c = canvas.Canvas(OUTPUT_FILE)
c.setPageSize((1319, 1800))

jpgPaths = os.listdir(OUTPUT_FOLDER)

def myCmp(a,b):
    return int(a.split('.')[0])-int(b.split('.')[0])
jpgPaths.sort(key=functools.cmp_to_key(myCmp))
for jpgPath in jpgPaths:
    c.drawImage(os.path.join(OUTPUT_FOLDER,jpgPath), 0, 0)
    print(jpgPath)
    c.showPage()
print("正在生成pdf。。。")
c.save()

# from PIL import Image
# pngPath = os.path.join(OUTPUT_FOLDER,str(1)+'.jpg')
# print(Image.open(pngPath).size)#(1319, 1800)
        