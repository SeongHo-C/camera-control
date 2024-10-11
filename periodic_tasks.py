import cv2
import os
from datetime import datetime

def save_camera_parameters(camera):
    parameters = {
        "밝기": cv2.CAP_PROP_BRIGHTNESS,
        "대비": cv2.CAP_PROP_CONTRAST,
        "채도": cv2.CAP_PROP_SATURATION,
        "색상": cv2.CAP_PROP_HUE,
        "선명도": cv2.CAP_PROP_SHARPNESS,
        "감마": cv2.CAP_PROP_GAMMA,
        "후광 보정": cv2.CAP_PROP_BACKLIGHT,
        "게인": cv2.CAP_PROP_GAIN,
        "확대/축소": cv2.CAP_PROP_ZOOM,
        "포커스": cv2.CAP_PROP_FOCUS,
        "노출": cv2.CAP_PROP_EXPOSURE,
    }

    current_time = datetime.now()
    date_str = current_time.strftime("%Y-%m-%d")
    time_str = current_time.strftime("%H:%M:%S")

    folder_path = "camera_parameters"
    os.makedirs(folder_path, exist_ok=True)

    filename = os.path.join(folder_path, f"{date_str}.txt").replace("-", "")

    with open(filename, "a") as f:  # 'a' 모드로 파일 열기 (append)
        if os.stat(filename).st_size == 0:  # 파일이 비어있으면 헤더 추가
            headers = ["생성일"] + list(parameters.keys())
            f.write(", ".join(headers) + "\n")
                
        values = [f"{date_str} {time_str}"] + [str(camera.get(prop)) for prop in parameters.values()]
        f.write(", ".join(values) + "\n")
        
def perform_periodic_tasks(camera):
    save_camera_parameters(camera)