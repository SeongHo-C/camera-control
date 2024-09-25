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
        self.cap = cv2.VideoCapture(1)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
        self.running = False
        self.recording = False
        self.fps = 30
        self.output = None
        self.start_time = None

    def run(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                # 현재 프레임이 수신되었음을 GUI에 알리고, 그 프레임을 신호와 함께 전송
                self.change_pixmap_signal.emit(frame)
                if self.recording:
                    # VideoWriter 객체 생성 여부 확인
                    if self.output is None:
                        self.start_new_recording()
                    self.output.write(frame)

                    if datetime.now() - self.start_time > timedelta(minutes=10):
                        self.stop_current_recording()
                        self.start_new_recording()
    
    def start(self):
        self.running = True
        # 새 스레드를 생성하고 시작하는 핵심적인 부분, 이를 통해 run() 메서드가 별도의 스레드에서 실행
        super().start()

    # def stop(self):
    #     self.running = False
    #     self.stop_recording()
    #     self.wait()
    #     self.cap.release()

    def start_recording(self):
        self.recording = True
        self.start_new_recording()

    def stop_recording(self):
        self.recording = False
        self.stop_current_recording()              

    def start_new_recording(self):
        self.start_time = datetime.now()
        date_str = self.start_time.strftime("%Y%m%d")
        time_str = self.start_time.strftime("%H%M%S")
        
        folder_path = os.path.join("recordings", date_str)
        os.makedirs(folder_path, exist_ok=True)
        
        file_name = f"{time_str}.avi"
        file_path = os.path.join(folder_path, file_name)
        
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.output = cv2.VideoWriter(file_path, fourcc, self.fps, (1280, 960))

    def stop_current_recording(self):
        if self.output is not None:
            self.output.release()
            self.output = None