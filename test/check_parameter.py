import cv2

# 카메라 초기화
cap = cv2.VideoCapture(1)

# 파라미터 목록 및 해당 OpenCV 속성
parameters = {
    "Brightness": cv2.CAP_PROP_BRIGHTNESS,
    "Contrast": cv2.CAP_PROP_CONTRAST,
    "Saturation": cv2.CAP_PROP_SATURATION,
    "Hue": cv2.CAP_PROP_HUE,
    "Sharpness": cv2.CAP_PROP_SHARPNESS,
    "Gamma": cv2.CAP_PROP_GAMMA,
    "White Balance": cv2.CAP_PROP_WHITE_BALANCE_BLUE_U,
    "Backlight Contrast": cv2.CAP_PROP_BACKLIGHT,
    "Exposure": cv2.CAP_PROP_EXPOSURE
}

# 파라미터 기본값 출력
print("Default Camera Parameters:")
for param_name, param_id in parameters.items():
    value = cap.get(param_id)
    if value != -1:  # 파라미터가 지원되는 경우에만 출력
        print(f"{param_name}: {value}")

# 카메라 해제
cap.release()