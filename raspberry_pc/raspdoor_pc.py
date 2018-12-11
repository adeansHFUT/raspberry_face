# coding=UTF-8
__author__ = '杨俊杰'
import requests

key = "your key"
secret = "your secret"
http_url_detect = "https://api-cn.faceplusplus.com/facepp/v3/detect"
http_url_create = "https://api-cn.faceplusplus.com/facepp/v3/faceset/create"
http_url_addface = "https://api-cn.faceplusplus.com/facepp/v3/faceset/addface"
http_url_setuserid = "https://api-cn.faceplusplus.com/facepp/v3/face/setuserid"


filepath = "yangjunjie.jpg"
filename = "yangjunjie"

#函数中所有的if else 其实都应该用try except
def detect_faces(filepath):  # 传入图片文件,返回检测到人脸的face_token
    """探测人脸返回各种信息"""
    files = {"image_file": open(filepath, "rb")}
    data = {"api_key": key, "api_secret": secret }
    response = requests.post(http_url_detect, data = data, files = files)
    req_dict = response.json()
    if req_dict['faces']:
        print('探测人脸成功, face_token为：'+ req_dict['faces'][0]['face_token'])
        return req_dict['faces'][0]['face_token']
    else:
        print('探测人脸失败')
        exit()

def set_faceset(outer_id):  # 创建face_set,返回outer_id
    params = {
        'api_key': key,
        'api_secret': secret,
        'outer_id' : outer_id,
    }
    response = requests.post(http_url_create, data=params)
    req_dict = response.json()
    if req_dict['faceset_token']:
        print("创建faceset成功,id为: " +req_dict['outer_id'])
        return req_dict['outer_id']
    else:
        print('创建失败')
        exit()


def addface(faceset_id,facetokens):#将face加入到faceset
    params = {
            'api_key':key,
            'api_secret':secret,
            'outer_id':faceset_id,
            'face_tokens':facetokens
            }
    r = requests.post(http_url_addface,data = params)
    req_dict = r.json()
    if req_dict['face_added'] :
        print("成功加入" , req_dict['face_added'] ,"个人脸")
        print( faceset_id+"中人脸数量:" , req_dict['face_count'] )
    else:
        print('添加人脸失败')
        exit()


def face_SetUserID(face_token,user_id):#为检测出的某一个人脸添加标识信息，该信息会在Search接口结果中返回，用来确定用户身份。
    params = {
            'api_key':key,
            'api_secret':secret,
            'face_token':face_token,
            'user_id':user_id
            }
    r = requests.post(http_url_setuserid,data = params)
    req_dict = r.json()
    if req_dict['user_id'] :
        print('修改用户名:'+ req_dict['user_id'] + "成功")


if __name__ == "__main__" :
    #outer_id = set_faceset('myset_1')
    face_token = detect_faces(filepath)
    addface('myset_1', face_token)
    face_SetUserID(face_token , filename)
