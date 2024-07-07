from PyQt5 import QtWidgets, QtGui, QtCore
from ai.car import vehicle_detect
from monitor.mdui import Ui_Dialog
from monitor.monitorframe import MonitorDialog
from monitor.monitorframe1 import MonitorDialog1
import data.resources_rc



class MainDialog(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.label = QtWidgets.QLabel(self)
        self.setCentralWidget(self.label)
        self.pixmap = QtGui.QPixmap("data/1.jpeg")
        # 设置QLabel的尺寸
        self.label.resize(self.width(), self.height())
        self.label.setScaledContents(True)
        # 将背景图片设置为QLabel的内容
        self.label.setPixmap(self.pixmap.scaled(self.label.size(), aspectRatioMode=QtCore.Qt.KeepAspectRatio,
                                                transformMode=QtCore.Qt.SmoothTransformation))
        # 监听窗口大小变化事件
        self.resizeEvent = self.on_resize
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)



    def on_resize(self, event):
        self.label.resize(self.width(), self.height())
        self.label.setPixmap(self.pixmap.scaled(self.label.size(), aspectRatioMode=QtCore.Qt.KeepAspectRatio,
                                                transformMode=QtCore.Qt.SmoothTransformation))

    def goin(self):
        self.monitorframe = MonitorDialog()
        self.monitorframe.show()
        self.close()

    def goin1(self):
        self.monitorframe1 = MonitorDialog1()
        self.monitorframe1.show()
        self.close()
