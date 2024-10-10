import cv2

def test_camera_parameters():
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    
    if not cap.isOpened():
        print("카메라를 열 수 없습니다")
        return

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

    # 수동 모드 전환
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
    cap.set(cv2.CAP_PROP_AUTO_WB, 0)
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)

    for name, prop in parameters.items():
        print(f"\n=== {name} (속성 ID: {prop}) 테스트 ===")
        
        current = cap.get(prop)
        print(f"현재 값: {current}")
        
        test_ranges = [
            (-10000, -5000, -1000, -500, -100, -50, -10),  
            (-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5),     
            (10, 50, 100, 500, 1000, 5000, 10000),  
        ]
        
        for value_range in test_ranges:
            for value in value_range:
                cap.set(prop, value)
                actual = cap.get(prop)
                if actual != current:  
                    print(f"설정 시도값: {value}, 실제 설정값: {actual}")
                    current = actual

    # 특별한 경우: 자동 노출/화이트밸런스/포커스 모드 전환 테스트
    auto_parameters = {
        "자동 노출": cv2.CAP_PROP_AUTO_EXPOSURE,
        "자동 화이트밸런스": cv2.CAP_PROP_AUTO_WB,
        "자동 포커스": cv2.CAP_PROP_AUTOFOCUS
    }
    
    print("\n=== 자동 모드 테스트 ===")
    for name, prop in auto_parameters.items():
        print(f"\n{name} (속성 ID: {prop})")
        for value in [0, 1, 2, 3]:  # 일반적인 자동/수동 모드 값
            cap.set(prop, value)
            actual = cap.get(prop)
            print(f"설정 시도값: {value}, 실제 설정값: {actual}")

    cap.release()

if __name__ == '__main__':
    test_camera_parameters()