import sys
import cv2
import numpy as np
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QSlider, QPushButton, QVBoxLayout, QGridLayout, QWidget, QHBoxLayout, QTabWidget, QCheckBox
from video_thread import VideoThread
from styles import button_style

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("카메라 제어 프로그램")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)

        self.video_label = QLabel(self)
        self.main_layout.addWidget(self.video_label)

        self.tabs = QTabWidget()
        self.main_layout.addWidget(self.tabs)

        self.recording_label = QLabel(self)
        self.recording_label.setAlignment(Qt.AlignCenter)

        camera_icon = QPixmap('./images/camera.png')
        self.recording_label.setPixmap(camera_icon)
        self.recording_label.setStyleSheet("color: red; font-size: 16px")
        self.recording_label.setText('촬영중')

        self.main_layout.addWidget(self.recording_label)
        # self.recording_label.hide()

# 비디오 프로세서 앰프 ------------------------------------------------------------------------------------------------         
        self.video_amp_tab = QWidget()
        self.tabs.addTab(self.video_amp_tab, "비디오 프로세서 앰프")
        self.video_amp_layout = QVBoxLayout(self.video_amp_tab)

        self.video_amp_slider_widget = QWidget()
        self.video_amp_slider_layout = QGridLayout(self.video_amp_slider_widget)
        self.video_amp_slider_widget.setLayout(self.video_amp_slider_layout)

        self.video_amp_layout.addWidget(self.video_amp_slider_widget)

        self.video_amp_sliders = {}
        self.video_amp_slider_labels = {}
        self.video_amp_parameters = {
            "밝기(B)": (cv2.CAP_PROP_BRIGHTNESS, -64, 64, 1, 0),
            "대비(C)": (cv2.CAP_PROP_CONTRAST, 0, 95, 1, 0),
            "채도(S)": (cv2.CAP_PROP_SATURATION, 0, 255, 1, 100),
            "색상(H)": (cv2.CAP_PROP_HUE, -2000, 2000, 1, 0),
            "선명도(P)": (cv2.CAP_PROP_SHARPNESS, 0, 7, 1, 0),
            "감마(G)": (cv2.CAP_PROP_GAMMA, 64, 300, 1, 100),
            "화이트 밸런스(W)": (cv2.CAP_PROP_WHITE_BALANCE_BLUE_U, 0, 1, 1, 0),
            "후광 보정(B)": (cv2.CAP_PROP_BACKLIGHT, 36, 160, 1, 50),
        }
        self.create_sliders(self.video_amp_parameters, self.video_amp_sliders, self.video_amp_slider_labels, self.video_amp_slider_layout)

        self.auto_wb_checkbox = QCheckBox("화이트 밸런스 자동")
        self.video_amp_slider_layout.addWidget(self.auto_wb_checkbox, len(self.video_amp_parameters), 0, 1, 2)
        self.auto_wb_checkbox.stateChanged.connect(self.toggle_auto_wb)
# -------------------------------------------------------------------------------------------------------------------

# 카메라 컨트롤 ------------------------------------------------------------------------------------------------------
        self.camera_control_tab = QWidget()
        self.tabs.addTab(self.camera_control_tab, "카메라 컨트롤")
        self.camera_control_layout = QVBoxLayout(self.camera_control_tab)

        self.camera_control_slider_widget = QWidget()
        self.camera_control_slider_layout = QGridLayout(self.camera_control_slider_widget)
        self.camera_control_slider_widget.setLayout(self.camera_control_slider_layout)

        self.camera_control_layout.addWidget(self.camera_control_slider_widget)

        self.camera_control_sliders = {}
        self.camera_control_slider_labels = {}
        self.camera_control_parameters = {
            "확대/축소(Z)": (cv2.CAP_PROP_ZOOM, 0, 60, 1, 0),
            "포커스(F)": (cv2.CAP_PROP_FOCUS, 0, 1023, 1, 0),
            "노출(E)": (cv2.CAP_PROP_EXPOSURE, 1, 8188, 1, 1000),
        }
        self.create_sliders(self.camera_control_parameters, self.camera_control_sliders, self.camera_control_slider_labels, self.camera_control_slider_layout)

        self.auto_focus_checkbox = QCheckBox("포커스 자동")
        self.camera_control_slider_layout.addWidget(self.auto_focus_checkbox, len(self.camera_control_parameters), 0, 1, 2)
        self.auto_focus_checkbox.stateChanged.connect(self.toggle_auto_focus)

        self.auto_exposure_checkbox = QCheckBox("노출 자동")
        self.camera_control_slider_layout.addWidget(self.auto_exposure_checkbox, len(self.camera_control_parameters) + 1, 0, 1, 2)
        self.auto_exposure_checkbox.stateChanged.connect(self.toggle_auto_exposure)
# -------------------------------------------------------------------------------------------------------------------

# 버튼 --------------------------------------------------------------------------------------------------------------
        self.button_layout = QHBoxLayout()
        self.main_layout.addLayout(self.button_layout) 

        self.start_button = QPushButton("촬영 시작")
        self.stop_button = QPushButton("촬영 중지")

        button_style(self.start_button)
        button_style(self.stop_button)

        self.start_button.clicked.connect(self.start_recording)
        self.stop_button.clicked.connect(self.stop_recording)

        self.button_layout.addWidget(self.start_button)
        self.button_layout.addWidget(self.stop_button)
# -------------------------------------------------------------------------------------------------------------------
    
        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()

    def create_sliders(self, parameters, sliders, slider_labels, slider_layout):
        for i, (name, (prop, min_val, max_val, step, default)) in enumerate(parameters.items()):
            slider = QSlider(Qt.Horizontal)
            slider.setRange(min_val, max_val)
            slider.setValue(default)
            slider.setTickPosition(QSlider.TicksBelow)
            slider.setTickInterval((max_val - min_val) // 10)
            slider.valueChanged.connect(lambda v, p=prop, n=name: self.update_camera_setting(p, v, n, slider_labels))
            
            sliders[prop] = slider
            label = QLabel(f"{name}: {default}")
            slider_labels[name] = label
            
            slider_layout.addWidget(label, i, 0)
            slider_layout.addWidget(slider, i, 1)

    def update_camera_setting(self, prop, value, name, slider_labels):
        self.thread.cap.set(prop, value)
        actual_value = self.thread.cap.get(prop)
        slider_labels[name].setText(f"{name}: {int(actual_value)}")

    def toggle_auto_wb(self, state):
        if state == Qt.Checked:
            self.thread.cap.set(cv2.CAP_PROP_AUTO_WB, 1)
            self.video_amp_sliders[cv2.CAP_PROP_WHITE_BALANCE_BLUE_U].setEnabled(False)
        else:
            self.thread.cap.set(cv2.CAP_PROP_AUTO_WB, 0)
            self.video_amp_sliders[cv2.CAP_PROP_WHITE_BALANCE_BLUE_U].setEnabled(True)

    def toggle_auto_focus(self, state):
        if state == Qt.Checked:
            self.thread.cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
            self.camera_control_sliders[cv2.CAP_PROP_FOCUS].setEnabled(False)
        else:
            self.thread.cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
            self.camera_control_sliders[cv2.CAP_PROP_FOCUS].setEnabled(True)

    def toggle_auto_exposure(self, state):
        if state == Qt.Checked:
            self.thread.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3)
            self.camera_control_sliders[cv2.CAP_PROP_EXPOSURE].setEnabled(False)
        else:
            self.thread.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
            self.camera_control_sliders[cv2.CAP_PROP_EXPOSURE].setEnabled(True)  

    def start_recording(self):
        self.thread.start_capturing()

    def stop_recording(self):
        self.thread.stop_capturing()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        qt_img = self.convert_cv_qt(cv_img)
        self.video_label.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(800, 600, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())