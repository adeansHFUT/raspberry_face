# coding=UTF-8
__author__ = '杨俊杰'
import requests

key = "your key"
secret = "your secret"
http_url_detect = "https://api-cn.faceplusplus.com/facepp/v3/detect"
http_url_search = "https://api-cn.faceplusplus.com/facepp/v3/search"

filepath3 = "jiege.jpg"


def detect_faces(filepath):  # 传入图片文件
    """探测人脸返回各种信息"""
    files = {"image_file": open(filepath, "rb")}
    data = {"api_key": key, "api_secret": secret, "return_attributes" : "age,emotion,beauty"}
    response = requests.post(http_url_detect, data = data, files = files)
    req_dict = response.json()
    return req_dict

def search_faces(face_token , outer_id):   #传入face_token
    """返回找到的user_id"""
    data = {"api_key": key, "api_secret": secret , 'face_token' : face_token , 'outer_id' : outer_id }
    response = requests.post(http_url_search, data = data)
    req_dic =response.json()
    return req_dic


if __name__ == "__main__":
    print(detect_faces(filepath3))
