from PyQt5.QtCore import QThread
import cv2 as cv
from PyQt5.QtCore import pyqtSignal
from ai.car import vehicle_detect
from ai.car import vehicle_moduel
# 重写run()方法: 线程执行的内容
# Thread的实例对象.start()  run()就会自动执行
class Video(QThread):
    # 使用信号与槽槽函数向外传递数据
    #    发送者   Video
    #    信号类型  自定义信号类型(参数信号所能传递的数据)
    #    接收者   （线程所在的Dialog）
    #    槽函数   （接收者类：功能方法）
    send = pyqtSignal(int, int, int, bytes,int,int) #emit
    def __init__(self,video_id):
        super().__init__()
        # 准备工作
        self.th_id = 0
        if video_id == 'data/vd1.mp4':
            self.th_id = 1
        if video_id == 'data/vd2.mp4':
            self.th_id = 2
        self.dev = cv.VideoCapture(video_id)
        self.dev.open(video_id)

    def run(self):
        # 耗时操作
        while True:
            ret, frame = self.dev.read()
            frame, num = vehicle_detect(frame)
            if not ret:
                print('no')
            # car
            h, w, c = frame.shape
            img_bytes = frame.tobytes()
            self.send.emit(h, w, c, img_bytes,self.th_id,num)
            QThread.usleep(10000)


import cv2 as cv
from PyQt5.QtCore import QThread, pyqtSignal
import base64
import requests


class Videoo(QThread):
    send = pyqtSignal(int, int, int, bytes, int, list)  # 自定义信号，用于传递视频帧和车辆信息

    def __init__(self, video_id):
        super().__init__()
        self.th_id = 0
        if video_id == 'data/vd1.mp4':
            self.th_id = 1
        elif video_id == 'data/vd2.mp4':
            self.th_id = 2
        else:
            raise ValueError(f"不支持的视频文件: {video_id}")

        self.dev = cv.VideoCapture(video_id)
        if not self.dev.isOpened():
            raise ValueError(f"无法打开视频文件: {video_id}")

    def run(self):
        """
        线程的主运行方法，用于读取视频帧并发送处理后的图像数据和车辆信息。
        """
        while True:
            ret, frame = self.dev.read()
            if not ret:
                print('无法读取视频帧，视频结束或出错')
                self.dev.set(cv.CAP_PROP_POS_FRAMES, 0)  # 视频结束后从头开始播放
                continue  # 继续读取帧

            frame, vehicle_data = vehicle_moduel(frame)
            h, w, c = frame.shape
            img_bytes = frame.tobytes()
            self.send.emit(h, w, c, img_bytes, self.th_id, vehicle_data)
            QThread.usleep(10000)  # 暂停10毫秒以控制帧率

    def capture_frame_for_detection(self):
        """
        捕获当前帧并进行车辆检测。
        """
        ret, frame = self.dev.read()
        if not ret:
            print('无法读取视频帧')
            return None, []

        frame, vehicle_data = vehicle_moduel(frame)
        return frame, vehicle_data

    def stop(self):
        """
        停止线程并释放视频资源。
        """
        self.dev.release()
        print('视频读取结束，资源已释放')
        self.quit()
        self.wait()


