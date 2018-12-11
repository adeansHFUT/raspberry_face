树莓派人脸识别与搜索
==========
基于[旷视科技](https://www.faceplusplus.com.cn/)face++的api
## 环境
树莓派3b<br>
raspbian
## 预装库和驱动
usb摄像头驱动<br>
vnc远程桌面驱动<br>
opencv库
## 用法
运行raspberry_door中的pick_camera.py可以识别人脸<br>
运行raspberry_pc中的raspberry_pc.py可以向自己的set添加人脸token（图片放在该目录）
## 可以做到
判断出人并识别出他是否在我们的set中<br>
情绪识别<br>
年龄识别<br>
颜值评分
## 还存在的问题
调用cv中识别人脸分类器时卡顿（可能由于树莓派本身性能所致）<br>
加入多线程后问题无法解决反而加重。。。
