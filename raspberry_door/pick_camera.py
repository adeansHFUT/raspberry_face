# coding=UTF-8
__author__ = '杨俊杰'

import cv2
import time
import analysis_js
import threading
from analysis_js import analysis_show

img_path = './pic/test.jpg'
font = cv2.FONT_HERSHEY_COMPLEX_SMALL#字体设置
lock = threading.Lock()

def camera_reader():
    face_times=0
    face_right = 0
    faces = []
    user_name = ''
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')#载入脸的特征
    capInput = cv2.VideoCapture(0)#开摄像头
    capInput.set(3, 640)  # set video width
    capInput.set(4, 480)  # set video height
    success, img = capInput.read()#摄像头获取该帧图像
    success, img = capInput.read()  # 摄像头获取该帧图像
    while success and face_right <= 25 and cv2.waitKey(1) != 27:  #这里waitKey(1)有一毫秒延时才能正常显示图像
        if face_times >= 50 :  # 视频中有脸时请求API,不用加框
            face_times = 0
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 图像灰化
            faces = faceCascade.detectMultiScale(gray, 1.1, 7)  # 识别人脸
            if len(faces) != 0 :
                cv2.imwrite(img_path, img)  # 写入该帧图像文件
                user_name = analysis_show(img_path, img, 1)  # 根据新img分析，把文本写入img
        if len(faces) != 0 and face_times != 0:
            user_name = analysis_show(img_path, img , 0) #把文本写入img（延时显示）
        cv2.imshow("ImageCaptured", img)
        face_times = face_times + 1
        if user_name != 'face_error' and user_name != '' and user_name != 'stranger':
            face_right = face_right + 1
        success, img = capInput.read()  # 摄像头获取该帧图像

    capInput.release()
    cv2.destroyAllWindows()
    return user_name


def camerea_show():
    success, img = capInput.read()  # 摄像头获取该帧图像
    global img
    global face_ok
    global face_times
    global face_right
    while success  and face_right == 0 and cv2.waitKey(1) != 27:  # 这里waitKey(1)有一毫秒延时才能正常显示图像
        if face_ok == 1:
            analysis_show(img_path, img, 0)  # 把文本写入img
        else:
            lock.acquire()
            cv2.putText(img, "no face", (100, 50), font, 1.2, (255, 255, 255), 1)
            lock.release()
        cv2.imshow("ImageCaptured", img)
        face_times = face_times + 1
        if face_times >= 50 :  # 请求识别人脸间隔
            face_times = 0
        lock.acquire()
        success, img = capInput.read()  # 摄像头获取该帧图像
        lock.release()

def detect_analysis():
    global face_times
    global face_ok
    global img
    global face_right
    faces = []
    user_name = ''
    while(1):
        if face_times >= 20:
            face_times = 0
            lock.acquire()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 图像灰化
            faces = faceCascade.detectMultiScale(gray, 1.1, 7)  # 识别人脸
            lock.release()
            if len(faces) != 0 :
                face_ok = 1
                lock.acquire()
                cv2.imwrite(img_path, img)  # 写入该帧图像文件
                lock.release()
                user_name = analysis_show(img_path, img, 1)  # 根据新img分析更新face_information
            else:
                face_ok = 0
        if user_name != 'face_error' and user_name != '' and user_name != 'stranger' and face_times >= 15:
            face_right = 1
            break
if __name__=='__main__':
        face_times = 0
        face_ok = 0
        face_right = 0
        analysis_js.name = ''
        analysis_js.face_information = {}
        faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')  # 载入脸的特征
        capInput = cv2.VideoCapture(0)  # 开摄像头
        capInput.set(3, 640)  # set video width
        capInput.set(4, 480)  # set video height
        success, img = capInput.read()  # 摄像头获取该帧图像
        t1 = threading.Thread(target= camerea_show)
        t2 = threading.Thread(target= detect_analysis)
        t1.start()
        t2.start()

