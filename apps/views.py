from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import *
from django.contrib.auth import get_user_model, authenticate, logout
from django.contrib.auth import login
from apps import work
User = get_user_model()
NAME = None

import json
import numpy as np
import base64
import os
import sys
import cv2
import base64


def image_to_base64(image_np):
    image = cv2.imencode('.jpg', image_np)[1]
    image_code = str(base64.b64encode(image))[2:-1]

    return image_code
# Create your views here.
#渲染登陆页面
def index_view(request):

    return render(request, 'login.html')
#
# def register1_view(request):
#     #获取当前请求方式
#     m = request.method
#
#     return HttpResponse(m)

# def register_view(request):
#     #根据请求方式处理不同的业务需求
#     m = request.method
#     if m =='GET':
#         return render(request, 'register.html')
#     else:
#         uname = request.POST.get('uname', '')
#         pwd = request.POST.get('pwd', '')
#         if  uname and pwd:
#
#             stu = User(sname=uname,spwd=pwd)
#             stu.save()
#             return HttpResponse("注册成功")
#         return HttpResponse("注册失败")
#处理登录
def login_view(request):
    m = request.method
    if m == 'GET':
        return render(request, 'login.html')

    #接收请求参数
    else:
        uname = request.POST.get('uname', '')
        pwd = request.POST.get('pwd', '')
        #查询数据库
        user = authenticate(username=uname, password=pwd)
        if user:
            login(request, user)
            return HttpResponseRedirect("/home/")
                    # render(request, 'home1.html')
        return HttpResponse('登录失败')

def home_view(request):
    if request.user.is_authenticated:
        warning = Warning.objects.values()
        device = DeInfo.objects.values()
        return render(request, 'home1.html',{'warning':warning,'device':device})
    else:
        return render(request, 'login.html')

def device_view(request):
    if request.user.is_authenticated:
        device = DeInfo.objects.values()
        return render(request, 'device1.html',{'device':device})
    else:
        return render(request, 'login.html')


def warning_view(request):
    if request.user.is_authenticated:
        warning = Warning.objects.values()
        return render(request, 'warning1.html',{'warning':warning})
    else:
        return render(request, 'login.html')

def device_list(request):

    return HttpResponse()


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")




def uploadInfo(request):
    if request.method == 'POST':
        req = json.loads(request.body)  # 将json编码的字符串再转换为python的数据结构
        address = req['address']
        id = req['id']
        img_str = req['image']  # 得到unicode的字符串
        img_decode_ = img_str.encode('ascii')  # 从unicode变成ascii编码
        img_decode = base64.b64decode(img_decode_)  # 解base64编码，得图片的二进制
        img_np_ = np.frombuffer(img_decode, np.uint8)
        img = cv2.imdecode(img_np_, cv2.COLOR_RGB2BGR)  # 转为opencv格式
        dt = datetime.now()
        dtw = dt.strftime("%Y-%m-%d %H:%M:%S")
        dtm =  dt.strftime("%Y%m%d%H%M%S")
        id1 = str(id)
        imname = id1+dtm
        img_dist,tem = work.fin(img)
        # img_dist = image_to_base64(img_dist)
        cv2.imwrite("img/"+imname+".jpg",img_dist)

        warn_inf = Warning(
            w_time = dtw,  # 拿到图片
            w_id = id,# 拿到图片的名字
            tem = tem,
            iname = imname

        )
        # warn_inf = Warning(w_time=dt,w_id=id,img = img_dist)
        warn_inf.save()
        return HttpResponse('添加成功！!')

    return HttpResponse('失败')
