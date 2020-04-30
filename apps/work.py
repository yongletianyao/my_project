#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
实现大津法
"""


import cv2
import numpy as np




def tuxiangzengqiang(img):
 (b, g, r) = cv2.split(img)
 img_bilateralblur1 = cv2.bilateralFilter(r, 3, 10, 15)  # 双边滤波
 img_bilateralblur2 = cv2.bilateralFilter(g, 3, 10, 15)  # 双边滤波
 img_bilateralblur3 = cv2.bilateralFilter(b, 3, 10, 15)  # 双边滤波
 clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(10, 10))
 img_clahe1 = clahe.apply(img_bilateralblur1)
 img_clahe2 = clahe.apply(img_bilateralblur2)
 img_clahe3 = clahe.apply(img_bilateralblur3)
 img_clahe = cv2.merge([img_clahe3, img_clahe2, img_clahe1])
 return img_clahe

#取前景
def backend(gray,back,r,g,b):
 for i in range(len(gray)):
  for j in range(len(gray[0])):
   if back[i][j] == 0:
    b[i][j] = 0
    g[i][j] = 0
    r[i][j] = 0
 return cv2.merge([b, g, r]),b,g,r#


#三通道分别KMEANS确定过温区域，返回模板
def k_means(r,g,b):
 res = np.zeros_like(r)
 res = res.reshape((-1, 1))
 data_r = r.reshape((-1, 1))
 data_r = np.float32(data_r)
 data_g = g.reshape((-1, 1))
 data_g = np.float32(data_g)
 data_b = b.reshape((-1, 1))
 data_b = np.float32(data_b)
 criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 0.5)
 flags = cv2.KMEANS_RANDOM_CENTERS
 compactness_r, labels_r, centers_r = cv2.kmeans(data_r, 4, None, criteria, 10, flags)
 centers_r = np.uint8(centers_r)
 compactness_g, labels_g, centers_g = cv2.kmeans(data_g, 4, None, criteria, 10, flags)
 centers_g = np.uint8(centers_g)
 compactness_b, labels_b, centers_b = cv2.kmeans(data_b, 4, None, criteria, 10, flags)
 centers_b = np.uint8(centers_b)
 cen_rmax = max(centers_r)
 cen_gmax = max(centers_g)
 cen_bmax = max(centers_b)
 res_r = centers_r[labels_r.flatten()]
 res_g = centers_g[labels_g.flatten()]
 res_b = centers_b[labels_b.flatten()]
 for i in range(len(res_r)):
  if res_r[i] == cen_rmax and res_g[i] == cen_gmax and res_b[i] == cen_bmax:
   res[i] = 255
  else:
   res[i] = 0
 # print(centers)
 dst1 = res.reshape((r.shape))
 return dst1

def fin(img):

 # img = cv2.imread("333.jpg", -1)
 img_dist = tuxiangzengqiang(img)
 gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 dist_flat = np.zeros_like(gray)
 retval, dst = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)#大津法二值化
 (b, g, r) = cv2.split(img)
 #去除噪声取前景模板
 kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4))
 closed = cv2.morphologyEx(dst, cv2.MORPH_CLOSE, kernel)
 closed = cv2.erode(closed, None, iterations=3)
 closed = cv2.dilate(closed, None, iterations=3)

 # image_merge = image_merge-255
 #print(dst)
 # cv2.imshow("src", img)
 # cv2.imshow("src", k_means(b))
 # cv2.imshow("src", k_means(g))

 img_result,b1,g1,r1 = backend(gray,closed,r,g,b)

 img_guowenquyu = k_means(r1,g1,b1)
 img_guowenquyu = cv2.medianBlur(img_guowenquyu, 3)
 kernel1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
 img_guowenquyu = cv2.morphologyEx(img_guowenquyu, cv2.MORPH_CLOSE, kernel1)

 #获取二值化图像连通域信息
 num_labels, labels, stats, centers = cv2.connectedComponentsWithStats(img_guowenquyu, connectivity=8, ltype=cv2.CV_32S)
 area = np.zeros(num_labels)
 for t in range(1, num_labels, 1):
  area[t] = stats[t][4]
  #求最大连通域
 a = np.argmax(area)
 x, y, w, h, area = stats[np.argmax(area)]

 cx, cy = centers[a]
 # 标出中心位置
 cv2.circle(img_dist, (np.int32(cx), np.int32(cy)), 2, (0, 255, 0), 2, 8, 0)
 # 画出外接矩形
 cv2.rectangle(img_dist, (x-5, y-5), (x + w+10, y + h+10), (0, 255, 0), 2, 8, 0)
 #在画框区域寻找最大灰度级
 tem_area = np.zeros((w,h))
 for i in range(w):
  for j in range(h):
   tem_area[i][j] = gray[y + j][x+i]
 _positon = max(map(max,tem_area))  # get the index of max in the a
 tem = _positon*100/255
 # cv2.imshow("img", img)
 # cv2.waitKey(0)
 return img_dist,tem
