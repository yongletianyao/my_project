import requests
import json
import numpy as np
import cv2
import base64


def getByte(path):
    with open(path, 'rb') as f:
        img_byte = base64.b64encode(f.read())  # 二进制读取后变base64编码
    img_str = img_byte.decode('ascii')  # 转成python的unicode
    return img_str


img_str = getByte('222.jpg')



requestsss = {'address': '1','id':'2', 'image': img_str}
req = json.dumps(requestsss)  # 字典数据结构变json(所有程序语言都认识的字符串)

res = requests.post('http://127.0.0.1:8000/upload/', data=req)
print(res.text)
