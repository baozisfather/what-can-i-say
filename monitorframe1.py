from PyQt5 import QtCore, QtGui, QtWidgets
from monitor.mfui1 import Ui_Dialog1
from monitor.Video import Videoo

class MonitorDialog1(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog1()
        self.ui.setupUi(self)

        self.th1 = Videoo('data/vd1.mp4')
        self.th1.send.connect(self.showimg)
        self.th1.start()

        # 绑定“识别车型”按钮事件
        self.ui.detectButton.clicked.connect(self.detect_vehicle)

    def showimg(self, h, w, c, b, th_id, vehicle_data):
        """
        处理来自 Videoo 线程的图像数据，并更新视频显示和车辆信息。
        """
        # 创建 QImage 对象，图像格式为 BGR888
        image = QtGui.QImage(b, w, h, w * c, QtGui.QImage.Format_BGR888)
        pix = QtGui.QPixmap.fromImage(image)

        if th_id == 1:
            # 自动缩放
            width = self.ui.video1.width()
            height = self.ui.video1.height()
            scale_pix = pix.scaled(width, height, QtCore.Qt.KeepAspectRatio)
            self.ui.video1.setPixmap(scale_pix)

            # 生成车辆信息文本
            vehicle_info_text = "\n".join([
                f"Type: {v.get('type', 'N/A')}, Color: {v.get('color', 'N/A')}, Year: {v.get('year', 'N/A')}"
                for v in vehicle_data
            ]) if vehicle_data else "没有车辆数据"

            # 更新文本信息
            self.ui.cardata.setText(vehicle_info_text)

    def detect_vehicle(self):
        """
        捕获当前帧并进行车辆识别。
        """
        frame, vehicle_data = self.th1.capture_frame_for_detection()  # 捕获当前帧并进行车型识别
        if frame is not None:
            print(f"捕获的车辆数据: {vehicle_data}")  # 调试信息
            vehicle_info_text = "\n".join([
                f"Type: {v.get('type', 'N/A')}, Color: {v.get('color', 'N/A')}, Year: {v.get('year', 'N/A')}"
                for v in vehicle_data
            ]) if vehicle_data else "没有车辆数据"
            self.ui.cardata.setText(vehicle_info_text)
        else:
            self.ui.cardata.setText("无法捕获当前帧")

    def closeEvent(self, event):
        """
        关闭对话框时调用 stop 方法，释放资源。
        """
        self.th1.stop()
        super().closeEvent(event)
