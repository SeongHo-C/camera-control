import cv2

cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

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
    "노출(E)": cv2.CAP_PROP_EXPOSURE
}

for param_name, param_id in parameters.items():
    value = cap.get(param_id)
    print(f"{param_name}: {value}")

cap.release()