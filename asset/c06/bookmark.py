from PyPDF2 import PdfFileReader as pdf_read
import json
#每个书签的索引格式
#{'/Title': '书签名', '/Page': '指向的目标页数', '/Type': '类型'}

text_outline_list = []
with open(r'D:\SelfStudy\Git\mldn.pdf', 'rb') as f:
    pdf = pdf_read(f)
    #检索文档中存在的文本大纲,返回的对象是一个嵌套的列表
    text_outline_list = pdf.getOutlines()
    print(text_outline_list)

titleDict = {}
chapterNum = 1
for dict in text_outline_list:
    titleDict[str(chapterNum)] = dict['/Title']
    chapterNum += 1

print(titleDict)

jsonStr = json.dumps(titleDict)
with open('Titles.json','w')as f:
    f.write(jsonStr)


with open('Titles.json','r')as f:
    testDict = json.load(f)
    print(testDict)
    print(type(testDict))