from PyQt5 import QtCore, QtGui, QtWidgets
from monitor.mfui import Ui_Dialog
from monitor.Video import Video  # 确保导入了 Video 类

class MonitorDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.th1 = Video('data/vd1.mp4')
        self.th1.send.connect(self.showimg)  # 绑定信号与槽函数
        self.th1.start()  # 启动线程

    def showimg(self, h, w, c, b, th_id, num):
        imgae = QtGui.QImage(b, w, h, w * c, QtGui.QImage.Format_BGR888)
        pix = QtGui.QPixmap.fromImage(imgae)
        if th_id == 1:
            # 自动缩放
            width = self.ui.video1.width()
            height = self.ui.video1.height()
            scale_pix = pix.scaled(width, height, QtCore.Qt.KeepAspectRatio)
            self.ui.video1.setPixmap(scale_pix)
            # str(num) 类型转换
            self.ui.carnum.setText(str(num))  # 更新车流量
