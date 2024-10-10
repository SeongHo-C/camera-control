import cv2
import numpy as np
import os
from datetime import datetime, timedelta
# QThread: 백그라운드 처리에 사용할 스레드를 생성하고 관리하는 데 사용
# pyqtSignal: 스레드 또는 객체 간의 통신을 위해 방출할 수 있는 신호
from PyQt5.QtCore import QThread, pyqtSignal

class VideoThread(QThread):
    # 신호가 전송할 데이터의 형식을 지정, 여기서는 NumPy 배열 형식의 데이터를 전달
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        self.cap.set(cv2.CAP_PROP_FPS, 90)

        actual_fps = self.cap.get(cv2.CAP_PROP_FPS)
        print(f'실제 설정 FPS: {actual_fps}')

        self.running = False
        self.capturing = False
        self.last_captured_time = None

    def run(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                # 현재 프레임이 수신되었음을 GUI에 알리고, 그 프레임을 신호와 함께 전송
                self.change_pixmap_signal.emit(frame)

                # 1초에 한 번만 캡처
                if self.capturing and (self.last_captured_time is None or (datetime.now() - self.last_captured_time).seconds >= 1):
                    self.capture_frame(frame)
                    self.last_captured_time = datetime.now()

    def start(self):
        self.running = True
        # 새 스레드를 생성하고 시작하는 핵심적인 부분, 이를 통해 run() 메서드가 별도의 스레드에서 실행
        super().start()

    def stop(self):
        self.running = False
        self.wait()
        self.cap.release()

    def start_capturing(self):
        self.capturing = True

    def stop_capturing(self):
        self.capturing = False

    def capture_frame(self, frame):
        current_time = datetime.now()
        
        date_str = current_time.strftime('%Y%m%d')
        time_str = current_time.strftime('%H%M%S')
        
        folder_path = os.path.join('captures', date_str)
        os.makedirs(folder_path, exist_ok=True)
        
        file_name = f'{time_str}.jpg'
        file_path = os.path.join(folder_path, file_name)
        
        cv2.imwrite(file_path, frame)