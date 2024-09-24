# Python 인터프리터와 상호작용하는 일부 변수 및 함수에 접근
import sys
import cv2
import numpy as np
# Qt: Qt에서 사용되는 열거형 및 상수를 포함
# QThread: 백그라운드 처리에 사용할 스레드를 생성하고 관리하는 데 사용
# pyqtSignal: 스레드 또는 객체 간의 통신을 위해 방출할 수 있는 신호
# pyqtSlot: 신호에 응답할 슬롯을 정의하기 위한 데코레이터
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
# GUI에서 이미지를 처리하고 픽스맵을 관리하기 위한 클래스
from PyQt5.QtGui import QImage, QPixmap
# GUI를 구축하기 위해 PyQt5에서 다양한 위젯 및 레이아웃
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QSlider, QPushButton, QVBoxLayout, QGridLayout, QWidget, QHBoxLayout, QTabWidget, QCheckBox

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(1)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        self.running = True

    def run(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                self.change_pixmap_signal.emit(frame)

    def stop(self):
        self.running = False
        self.wait()

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("카메라 제어 프로그램")
        # 모든 GUI 요소를 담는 기본 컨테이너로 사용되며, 다른 위젯들을 포함하여 복잡한 사용자 인터페이스를 구성하는 데 사용
        # 사용자 입력(클릭, 키 입력 등)에 대한 이벤트를 처리
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 중앙 위젯에 수직 박스 레이아웃을 설정하여 위젯들을 수직으로 배치
        self.main_layout = QVBoxLayout(self.central_widget)

        # 자식 위젯(하위 클래스)을 부모와 연결하여 올바르게 배치하고 관리 
        self.video_label = QLabel(self)
        self.main_layout.addWidget(self.video_label)

        # QTabWidget 객체 생성
        self.tabs = QTabWidget()
        self.main_layout.addWidget(self.tabs)

        # QTabWidget의 각 탭은 특정 위젯을 포함, 탭의 내용을 구성하기 위해 QWidget 생성
        self.video_amp_tab = QWidget()
        self.tabs.addTab(self.video_amp_tab, "비디오 프로세서 앰프")
        self.video_amp_layout = QVBoxLayout(self.video_amp_tab)

        # 슬라이더를 포함할 컨테이너 역할
        self.slider_widget = QWidget()
        # self.slider_widget을 매개변수로 넘겨줌으로써, 이 레이아웃이 slider_widget의 레이아웃이 되도록 설정(생성)
        self.slider_layout = QGridLayout(self.slider_widget)
        # slider_widget이 이 레이아웃을 사용하여 내부의 위젯들을 배치(적용)
        self.slider_widget.setLayout(self.slider_layout)

        self.video_amp_layout.addWidget(self.slider_widget)

        self.sliders = {}
        self.slider_labels = {}
        self.parameters = {
            "밝기(B)": (cv2.CAP_PROP_BRIGHTNESS, -64, 64, 1, 0),
            "대비(C)": (cv2.CAP_PROP_CONTRAST, 0, 95, 1, 0),
            "채도(S)": (cv2.CAP_PROP_SATURATION, 0, 255, 1, 66),
            "색상(H)": (cv2.CAP_PROP_HUE, -2000, 2000, 1, 0),
            "선명도(P)": (cv2.CAP_PROP_SHARPNESS, 0, 7, 1, 0),
            "감마(G)": (cv2.CAP_PROP_GAMMA, 64, 300, 1, 100),
            "화이트 밸런스(W)": (cv2.CAP_PROP_WHITE_BALANCE_BLUE_U, 2800, 6500, 1, 2800),
            "후광 보정(B)": (cv2.CAP_PROP_BACKLIGHT, 36, 160, 1, 84),
        }
        self.create_sliders()

        self.auto_wb_checkbox = QCheckBox("화이트 밸런스 자동")
        self.slider_layout.addWidget(self.auto_wb_checkbox, len(self.parameters), 0, 1, 2)  # 슬라이더 하단에 배치
        self.auto_wb_checkbox.stateChanged.connect(self.toggle_auto_wb)

        self.camera_control_tab = QWidget()
        self.tabs.addTab(self.camera_control_tab, "카메라 컨트롤")
        self.camera_control_layout = QVBoxLayout(self.camera_control_tab)

        self.slider_widget2 = QWidget()
        self.slider_layout2 = QGridLayout(self.slider_widget2)
        self.slider_widget2.setLayout(self.slider_layout2)

        self.camera_control_layout.addWidget(self.slider_widget2)

        self.sliders2 = {}
        self.slider_labels2 = {}
        self.parameters2 = {
            "포커스(F)": (cv2.CAP_PROP_FOCUS, 0, 1023, 1, 0),
            "노출(E)": (cv2.CAP_PROP_EXPOSURE, -13, 0, 1, -6),
        }
        self.create_sliders2()

        # 포커스 자동 설정 체크박스
        self.auto_focus_checkbox = QCheckBox("포커스 자동")
        self.slider_layout2.addWidget(self.auto_focus_checkbox, len(self.parameters2), 0, 1, 2)  # 카메라 컨트롤 탭에 배치
        self.auto_focus_checkbox.stateChanged.connect(self.toggle_auto_focus)

        # 노출 자동 설정 체크박스
        self.auto_exposure_checkbox = QCheckBox("노출 자동")
        self.slider_layout2.addWidget(self.auto_exposure_checkbox, len(self.parameters2) + 1, 0, 1, 2)
        self.auto_exposure_checkbox.stateChanged.connect(self.toggle_auto_exposure)

        self.button_layout = QHBoxLayout()
        self.main_layout.addLayout(self.button_layout) 

        self.start_button = QPushButton("촬영 시작")
        self.stop_button = QPushButton("촬영 중지")

        self.setup_button_style(self.start_button)
        self.setup_button_style(self.stop_button)

        self.button_layout.addWidget(self.start_button)
        self.button_layout.addWidget(self.stop_button)

        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()

    def create_sliders(self):
        for i, (name, (prop, min_val, max_val, step, default)) in enumerate(self.parameters.items()):
            slider = QSlider(Qt.Horizontal)
            slider.setRange(min_val, max_val)
            slider.setValue(default)
            slider.setTickPosition(QSlider.TicksBelow)
            slider.setTickInterval((max_val - min_val) // 10)
            slider.valueChanged.connect(lambda v, p=prop, n=name: self.update_camera_setting(p, v, n))
            
            self.sliders[prop] = slider
            label = QLabel(f"{name}: {default}")
            self.slider_labels[name] = label
            
            # 그리드 레이아웃에 레이블과 슬라이더 추가
            self.slider_layout.addWidget(label, i, 0)
            self.slider_layout.addWidget(slider, i, 1)

    def update_camera_setting(self, prop, value, name):
        self.thread.cap.set(prop, value)
        self.slider_labels[name].setText(f"{name}: {value}")

    def create_sliders2(self):
        for i, (name, (prop, min_val, max_val, step, default)) in enumerate(self.parameters2.items()):
            slider = QSlider(Qt.Horizontal)
            slider.setRange(min_val, max_val)
            slider.setValue(default)
            slider.setTickPosition(QSlider.TicksBelow)
            slider.setTickInterval((max_val - min_val) // 10)
            slider.valueChanged.connect(lambda v, p=prop, n=name: self.update_camera_setting2(p, v, n))
            
            self.sliders2[prop] = slider
            label = QLabel(f"{name}: {default}")
            self.slider_labels2[name] = label
            
            # 그리드 레이아웃에 레이블과 슬라이더 추가
            self.slider_layout2.addWidget(label, i, 0)
            self.slider_layout2.addWidget(slider, i, 1)

    def update_camera_setting2(self, prop, value, name):
        self.thread.cap.set(prop, value)
        self.slider_labels2[name].setText(f"{name}: {value}")

    def setup_button_style(self, button):
        button.setStyleSheet("""
          QPushButton {
              background-color: white; 
              color: black;               
              border: 1px solid gray;   
              border-radius: 5px;          
              padding: 5px 10px;           
          }
          QPushButton:hover {
              background-color: gray;
              color: white;  
          }
        """)

    def toggle_auto_wb(self, state):
      if state == Qt.Checked:
        self.thread.cap.set(cv2.CAP_PROP_AUTO_WB, 1)  # 화이트 밸런스 자동 활성화
        self.sliders[cv2.CAP_PROP_WHITE_BALANCE_BLUE_U].setEnabled(False)
      else:
        self.thread.cap.set(cv2.CAP_PROP_AUTO_WB, 0)  # 화이트 밸런스 자동 비활성화
        self.sliders[cv2.CAP_PROP_WHITE_BALANCE_BLUE_U].setEnabled(True)

    def toggle_auto_focus(self, state):
      if state == Qt.Checked:
        self.thread.cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)  # 포커스 자동 활성화
        self.sliders2[cv2.CAP_PROP_FOCUS].setEnabled(False)
      else:
        self.thread.cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)  # 포커스 자동 비활성화
        self.sliders2[cv2.CAP_PROP_FOCUS].setEnabled(True)

    def toggle_auto_exposure(self, state):
      if state == Qt.Checked:
        self.thread.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.75)  # 노출 자동 활성화
        self.sliders2[cv2.CAP_PROP_EXPOSURE].setEnabled(False)
      else:
        self.thread.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)  # 노출 자동 비활성화
        self.sliders2[cv2.CAP_PROP_EXPOSURE].setEnabled(True)

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
