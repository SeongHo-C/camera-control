import cv2
import os
from datetime import datetime

def save_camera_parameters(camera):
    # 저장할 카메라 파라미터 목록
    parameters = {
        "밝기(B)": cv2.CAP_PROP_BRIGHTNESS,
        "대비(C)": cv2.CAP_PROP_CONTRAST,
        "채도(S)": cv2.CAP_PROP_SATURATION,
        "색상(H)": cv2.CAP_PROP_HUE,
        "선명도(P)": cv2.CAP_PROP_SHARPNESS,
        "감마(G)": cv2.CAP_PROP_GAMMA,
        "후광 보정(B)": cv2.CAP_PROP_BACKLIGHT,
        "게인(G)": cv2.CAP_PROP_GAIN,
        "확대/축소(Z)": cv2.CAP_PROP_ZOOM,
        "포커스(F)": cv2.CAP_PROP_FOCUS,
        "노출(E)": cv2.CAP_PROP_EXPOSURE,
        "화이트밸런스 온도(W)": cv2.CAP_PROP_WB_TEMPERATURE
    }

    # 현재 날짜 및 시간 저장
    current_time = datetime.now()
    date_str = current_time.strftime("%Y%m%d")
    time_str = current_time.strftime("%H:%M:%S")

    # 날짜별 폴더 생성
    folder_path = "camera_parameters"
    os.makedirs(folder_path, exist_ok=True)

    # 해당 날짜의 파일 경로
    filename = os.path.join(folder_path, f"{date_str}.txt")

    # 파라미터 값을 텍스트 파일에 이어서 저장
    with open(filename, "a") as f:  # 'a' 모드로 파일 열기 (append)
        if os.stat(filename).st_size == 0:  # 파일이 비어있으면 헤더 추가
            f.write(f"Camera Parameters Log - {date_str}\n")
            f.write("-" * 40 + "\n")
        
        f.write(f"{time_str}\n")
        
        # 각 파라미터 값을 가져와서 저장
        for name, prop in parameters.items():
            value = camera.get(prop)
            f.write(f"{name}: {value}\n")
        
        f.write("\n")  # 각 기록 사이에 빈 줄 추가

    print(f"Camera parameters saved at {time_str} to {filename}")

def perform_periodic_tasks(camera):
    save_camera_parameters(camera)