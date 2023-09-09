# # from PySide2.QtWidgets import QWidget, QApplication, QSlider, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
# # from PySide2.QtCore import Qt, QTimer,QRect
# # from PySide2.QtGui import QPainter, QPixmap,QFont,QImage
# import sys
# import cv2
# import utils
# from gesture_detector import GestureDetector
# import con_signal
# from collections import defaultdict
# from pykalman import KalmanFilter
# import math

# # 创建一个摄像头捕获对象，使用默认的摄像头设备
# cap = cv2.VideoCapture(0)
# detecor = GestureDetector()

# # # 创建一个覆盖窗口类，用来显示手势反馈和摄像头画面
# # class OverlayWidget(QWidget):

# #     def __init__(self):
# #         QWidget.__init__(self, geometry=QApplication.desktop().screenGeometry())

# #         self.setAttribute(Qt.WA_TranslucentBackground)
# #         self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
# #         self.frame = None
# #         # 创建一个定时器，用来定时更新窗口的内容
# #         timer = QTimer(self)
# #         timer.timeout.connect(self.update)
# #         timer.start(10)
# #         self.cmd_history = []
# #         self.cmd_history_max_len = 5

# #         # 初始化手势图像和文字的字典，用来存储不同手势对应的图像和文字
# #         self.gesture_img_dict = {
# #             "up": QPixmap("./source/speedup.png"),
# #             "left": QPixmap("./source/left.png"),
# #             "right": QPixmap("./source/right.png"),
# #             "bark": QPixmap("./source/bark.png"),
# #             "unknown": QPixmap("unknow.png")
# #         }
# #         self.gesture_text_dict = {
# #             "up": "加速",
# #             "bark": "刹车",
# #             "left": "左转",
# #             "right": "右转",
# #             "unknown": "未知"
# #         }

# #         # 初始化当前手势图像和文字为未知
# #         self.gesture_img = self.gesture_img_dict["unknown"]
# #         self.gesture_text = self.gesture_text_dict["unknown"]

# #         self.kf = KalmanFilter(transition_matrices=1, observation_matrices=1)
  
# #         # kalman
# #         self.kf.initial_state_mean = 0 
# #         self.kf.initial_state_covariance = 1

# #         self.kf.transition_covariance = 0.001
# #         self.kf.observation_covariance = 0.5

# #         self.observation = 1 

# #     def get_most_frequent(self):  
# #         count = defaultdict(int)  
# #         for cmd_str in self.cmd_history:
# #             count[cmd_str] += 1
# #         most_common = max(count, key=count.get)
# #         self.cmd_history=[]
# #         return  most_common

# #     def stable_sigmoid(self,x):
# #         a = 0.05
# #         if x >= 0:
# #             z = math.exp(-a*x)
# #             sig = 1 / (1 + z)
# #             return sig-0.5
# #         else:
# #             z = math.exp(a*x)
# #             sig = z / (1 + z)
# #             return sig-0.5

# #     def update(self):
        
# #         ret, frame = cap.read()
# #         if not ret:
# #             return
# #         frame= cv2.flip(frame,1)

# #         self.frame = detecor.findHands(frame)
# #         detecor.findPosition(self.frame)
# #         gesture = utils.update_gesture_status_low(detecor)

# #         cmd1='unknown'
# #         cmd2='unknown'
        
# #         self.kf.transition_matrices = 1
# #         self.kf.observation_matrices = self.observation
# #         filtered_angle = self.kf.filter(gesture['Angle'])[0][0][0]
# #         filtered_angle = self.stable_sigmoid(filtered_angle)
# #         filtered_angle = filtered_angle*2
# #         print(filtered_angle)
# #         signal = {
# #             "up":False,
# #             "bark":False,
# #             "Angle":filtered_angle
# #         }

# #         if(gesture['Left Thumb']):
# #             cmd2 = 'bark'
# #             signal["bark"] = True
# #         elif(gesture['Right Thumb']):
# #             cmd2 = 'up'
# #             signal["up"] = True
# #         if(filtered_angle<-0.25):
# #             cmd1 = 'left'
# #         elif(filtered_angle>0.25):
# #             cmd1 = 'right'

# #         self.cmd_history.append(cmd1 + '_' + cmd2)
        
# #         if len(self.cmd_history) > self.cmd_history_max_len:

# #             gmf = self.get_most_frequent()
            
# #             cmd1, cmd2 = gmf.split('_')

# #             # 根据手势类别，从字典中获取对应的图像和文字
# #             if(cmd1!='unknown'):
# #                 self.gesture_img = self.gesture_img_dict.get(cmd1, self.gesture_img_dict["unknown"])
# #                 self.gesture_text = self.gesture_text_dict.get(cmd1, self.gesture_text_dict["unknown"])
# #             elif(cmd2!='unknown'):
# #                 self.gesture_img = self.gesture_img_dict.get(cmd2, self.gesture_img_dict["unknown"])
# #                 self.gesture_text = self.gesture_text_dict.get(cmd2, self.gesture_text_dict["unknown"])
# #             else:
# #                 self.gesture_img = self.gesture_img_dict.get('unknow', self.gesture_img_dict["unknown"])
# #                 self.gesture_text = self.gesture_text_dict.get('unknow', self.gesture_text_dict["unknown"])
# #             print(f"Detected gesture: {gesture}")
# #             con_signal.gamepad_Control(signal)
# #             # 更新窗口的绘制
# #         self.repaint()
    
# #     def paintEvent(self, event):
# #         painter = QPainter(self)

# #         opacity = 0.8
# #         painter.setOpacity(opacity)
        
# #         rect = self.gesture_img.rect()
# #         rect.moveCenter(self.rect().center())
# #         painter.drawPixmap(rect.topLeft(), self.gesture_img)

        
# #         painter.setFont(QFont("Arial", 20))
# #         painter.drawText(self.rect(), Qt.AlignBottom | Qt.AlignHCenter, self.gesture_text)

# #         img = QImage(self.frame.data, self.frame.shape[1], self.frame.shape[0], 
# #                     self.frame.strides[0], QImage.Format_RGB888)
                    
# #         img_width = img.width() // 2
# #         img_height = img.height() // 2
# #         camera_rect = QRect(0, 0, 
# #                             img_width, img_height)
                            
# #         # 绘制图像                
# #         painter.drawImage(camera_rect, img)

# # # 创建一个主窗口类，用来显示灵敏度调节和退出按钮
# # class MainWindow(QWidget):

# #     def __init__(self):
# #         QWidget.__init__(self)

# #         # 创建一个滑动条用来调节手势识别的灵敏度
# #         self.sensitivity_slider = QSlider(Qt.Horizontal)
# #         self.sensitivity_slider.setMinimum(0)
# #         self.sensitivity_slider.setMaximum(100)
# #         self.sensitivity_slider.setValue(50) # 默认值为50
# #         self.sensitivity_slider.valueChanged.connect(self.on_sensitivity_changed)

# #         # 标签
# #         self.sensitivity_label = QLabel("灵敏度: 50")

# #         # 按钮
# #         self.exit_button = QPushButton("退出")
# #         self.exit_button.clicked.connect(self.on_exit_clicked)

# #         self.hbox = QHBoxLayout()
# #         self.hbox.addWidget(self.sensitivity_slider)
# #         self.hbox.addWidget(self.sensitivity_label)

# #         self.vbox = QVBoxLayout()
# #         self.vbox.addLayout(self.hbox)
# #         self.vbox.addWidget(self.exit_button)

# #         self.setLayout(self.vbox)

# #     def on_sensitivity_changed(self, value):
# #         self.sensitivity_label.setText(f"灵敏度: {value}")
        

# #     def on_exit_clicked(self):
# #         # 关闭程序
# #         sys.exit()
    

# if __name__ == "__main__":
#    app = QApplication([]) 
# #    overlay_window = OverlayWidget()
# #    overlay_window.show()
# #    main_window = MainWindow()
# #    main_window.show()
#    app.exec_()

import cv2
import utils
from gesture_detector import GestureDetector
import con_signal
from collections import defaultdict
from pykalman import KalmanFilter
import math
import tkinter as tk
from PIL import Image, ImageTk

# 创建一个摄像头捕获对象，使用默认的摄像头设备
cap = cv2.VideoCapture(0)
detecor = GestureDetector()

# 创建一个覆盖窗口类，用来显示手势反馈和摄像头画面
class OverlayWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")
        self.attributes('-alpha', 0.8)
        self.overrideredirect(1)
        self.frame = None
        self.cmd_history = []
        self.cmd_history_max_len = 5

        self.gesture_img_dict = {
            "up": Image.open("./source/speedup.png"),
            "left": Image.open("./source/left.png"),
            "right": Image.open("./source/right.png"),
            "bark": Image.open("./source/bark.png"),
            "unknown": Image.open("./source/unknow.png")
        }
        self.gesture_text_dict = {
            "up": "加速",
            "bark": "刹车",
            "left": "左转",
            "right": "右转",
            "unknown": "未知"
        }

        self.gesture_img = self.gesture_img_dict["unknown"]
        self.gesture_text = self.gesture_text_dict["unknown"]

        self.kf = KalmanFilter(transition_matrices=1, observation_matrices=1)

        self.kf.initial_state_mean = 0
        self.kf.initial_state_covariance = 1

        self.kf.transition_covariance = 0.001
        self.kf.observation_covariance = 0.5

        self.observation = 1

        self.canvas = tk.Canvas(self, bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.update()

    def get_most_frequent(self):
        count = defaultdict(int)
        for cmd_str in self.cmd_history:
            count[cmd_str] += 1
        most_common = max(count, key=count.get)
        self.cmd_history = []
        return most_common

    def stable_sigmoid(self, x):
        a = 0.05
        if x >= 0:
            z = math.exp(-a * x)
            sig = 1 / (1 + z)
            return sig - 0.5
        else:
            z = math.exp(a * x)
            sig = z / (1 + z)
            return sig - 0.5

    def update(self):
        ret, frame = cap.read()
        if not ret:
            return
        frame = cv2.flip(frame, 1)

        self.frame = detecor.findHands(frame)
        detecor.findPosition(self.frame)
        gesture = utils.update_gesture_status_low(detecor)

        cmd1 = 'unknown'
        cmd2 = 'unknown'

        self.kf.transition_matrices = 1
        self.kf.observation_matrices = self.observation
        filtered_angle = self.kf.filter(gesture['Angle'])[0][0][0]
        filtered_angle = self.stable_sigmoid(filtered_angle)
        filtered_angle = filtered_angle * 2
        print(filtered_angle)
        signal = {
            "up": False,
            "bark": False,
            "Angle": filtered_angle
        }

        if gesture['Left Thumb']:
            cmd2 = 'bark'
            signal["bark"] = True
        elif gesture['Right Thumb']:
            cmd2 = 'up'
            signal["up"] = True
        if filtered_angle < -0.25:
            cmd1 = 'left'
        elif filtered_angle > 0.25:
            cmd1 = 'right'

        self.cmd_history.append(cmd1 + '_' + cmd2)

        if len(self.cmd_history) > self.cmd_history_max_len:
            gmf = self.get_most_frequent()

            cmd1, cmd2 = gmf.split('_')

            if cmd1 != 'unknown':
                # self.gesture_img = Image.open(self.gesture_img_dict.get(cmd1, self.gesture_img_dict["unknown"]))
                self.gesture_text = self.gesture_text_dict.get(cmd1, self.gesture_text_dict["unknown"])
            elif cmd2 != 'unknown':
                # self.gesture_img = Image.open(self.gesture_img_dict.get(cmd2, self.gesture_img_dict["unknown"]))
                self.gesture_text = self.gesture_text_dict.get(cmd2, self.gesture_text_dict["unknown"])
            else:
                # self.gesture_img = Image.open(self.gesture_img_dict.get('unknow', self.gesture_img_dict["unknown"]))
                self.gesture_text = self.gesture_text_dict.get('unknow', self.gesture_text_dict["unknown"])
            print(f"Detected gesture: {gesture}")
            con_signal.gamepad_Control(signal)
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.gesture_img_tk)
            self.canvas.create_text(
                self.winfo_width() // 2,
                self.winfo_height(),
                text=self.gesture_text,
                font=("Arial", 20),
                anchor=tk.S,
                fill="white"
            )

        self.gesture_img_tk = ImageTk.PhotoImage(self.gesture_img)
        self.after(10, self.update)

if __name__ == "__main__":
    overlay_window = OverlayWindow()
    overlay_window.mainloop()

