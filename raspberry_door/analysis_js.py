# coding=UTF-8
__author__ = '杨俊杰'
import cv2
import threading
from face_api import detect_faces
from face_api import search_faces
lock = threading.Lock()
font = cv2.FONT_HERSHEY_COMPLEX_SMALL#字体设置
face_information = {}
name = ''

"""cover为1则仅覆盖,cover为0则仅添加文字"""
def analysis_show(path, img , cover ):
    global face_information               #申明使用全局变量
    global name
    if cover:
        face_information = detect_faces(path)
        try :
            if face_information['faces']:
                name = search_show(face_information)
            return name
        except KeyError :
            print('no face')
    else:
        try:
            if face_information['faces']:
                # x = face_information['faces'][0]['face_rectangle']['left']
                # y = face_information['faces'][0]['face_rectangle']['top']
                age = face_information['faces'][0]['attributes']['age']['value']
                emotion = face_information['faces'][0]['attributes']['emotion']
                emotion = emotion.copy()    #操作复制的一份防止重复pop
                emotion1 = max(emotion , key = emotion.get)
                emotion.pop(emotion1)
                emotion2 = max(emotion , key=emotion.get)
                beauty = face_information['faces'][0]['attributes']['beauty']
                lock.acquire()
                show_info( name , img, age, emotion1, emotion2, beauty)
                lock.release()
            else:
                lock.acquire()
                cv2.putText(img, "no face", (100, 50), font, 1.2, (255, 255, 255), 1)  # 照片/添加的文字/左上角坐标/字体/字体大小/颜色/字体粗细
                lock.release()
        except KeyError :
            cv2.putText(img, "no face", (100, 50), font, 1.2, (255, 255, 255), 1)


"""人脸搜索返回user_id"""
def search_show(faces_information):
    face_search = search_faces(faces_information['faces'][0]['face_token'], 'myset_1') #需添加face_set的outer_id
    # if face_search['faces']:
    #     confidence = face_search['results'][0]['confidence']  # 读取置信度
    #     thresholds = face_search['thresholds']['1e-5']
    #     if confidence > 75 and thresholds < confidence:  # 置信度阈值判断
    #         return face_search['results'][0]['user_id']  # 获得唯一人脸id
    #     else:
    #         return 'stranger'
    #
    # else:
    #     return 'face_error'

    confidence = face_search['results'][0]['confidence']  # 读取置信度
    thresholds = face_search['thresholds']['1e-4']
    if confidence > 70 and thresholds < confidence:  # 置信度阈值判断
        return face_search['results'][0]['user_id']  # 获得唯一人脸id
    else:
        return 'stranger'


def show_info( name, img ,age , emotion1 , emotion2 , beauty):
    cv2.putText(img, "Name: " + name, (50, 20), font , 1 , (0 ,0 , 255) , 1)
    cv2.putText(img, "Age: "+ str(age), (50, 50), font, 1, (255, 255, 255), 1)  # 照片/添加的文字/左上角坐标/字体/字体大小/颜色/字体粗细
    cv2.putText(img, "Emotion: " + changeto_ch(emotion1) + "," + changeto_ch(emotion2) , (50, 80), font, 1, (255, 255, 255), 1)
    cv2.putText(img, "Beauty: " + 'Scores given by women: ' + str(beauty['female_score']) , (50, 110), font, 1, (255, 255, 255), 1)
    cv2.putText(img, "        " + 'Scores given by men: ' + str(beauty['male_score']) , (50, 140), font, 1, (255, 255, 255), 1)

def changeto_ch(text):
    #ascll转unicode（或者相反）
    return {
        'anger': 'anger',
        'disgust': 'disgust',
        'fear': 'fear',
        'happiness': 'happiness' ,
        'neutral': 'neutral' ,
        'sadness': 'sadness',
        'surprise': 'surprise' ,
    }.get(text, 'error')  # 'error'为默认返回值，可自设置

if __name__ == "__main__":
    print(analysis_show(path = "jiege.jpg"  ))
