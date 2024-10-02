import cv2
import numpy as np

def test_camera_parameters():
    # V4L2 백엔드를 명시적으로 사용
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    
    if not cap.isOpened():
        print("카메라를 열 수 없습니다")
        return

    # 테스트할 파라미터 목록
    parameters = {
        "밝기": cv2.CAP_PROP_BRIGHTNESS,
        "대비": cv2.CAP_PROP_CONTRAST,
        "채도": cv2.CAP_PROP_SATURATION,
        "색상": cv2.CAP_PROP_HUE,
        "선명도": cv2.CAP_PROP_SHARPNESS,
        "감마": cv2.CAP_PROP_GAMMA,
        "화이트밸런스": cv2.CAP_PROP_WHITE_BALANCE_BLUE_U,
        "후광보정": cv2.CAP_PROP_BACKLIGHT,
        "확대/축소": cv2.CAP_PROP_ZOOM,
        "포커스": cv2.CAP_PROP_FOCUS,
        "노출": cv2.CAP_PROP_EXPOSURE
    }

    # 각 파라미터에 대해 다양한 값을 시도
    for name, prop in parameters.items():
        print(f"\n=== {name} (속성 ID: {prop}) 테스트 ===")
        
        # 현재 값 확인
        current = cap.get(prop)
        print(f"현재 값: {current}")

        # cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
        # cap.set(cv2.CAP_PROP_AUTO_WB, 0)
        # cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
        
        # 자동 모드 확인 (노출, 화이트밸런스, 포커스)
        if prop in [cv2.CAP_PROP_EXPOSURE, cv2.CAP_PROP_WHITE_BALANCE_BLUE_U, cv2.CAP_PROP_FOCUS]:
            auto_prop = None
            if prop == cv2.CAP_PROP_EXPOSURE:
                auto_prop = cv2.CAP_PROP_AUTO_EXPOSURE
            elif prop == cv2.CAP_PROP_WHITE_BALANCE_BLUE_U:
                auto_prop = cv2.CAP_PROP_AUTO_WB
            elif prop == cv2.CAP_PROP_FOCUS:
                auto_prop = cv2.CAP_PROP_AUTOFOCUS
            
            if auto_prop is not None:
                auto_value = cap.get(auto_prop)
                print(f"자동 모드 상태: {auto_value}")
        
        # 값 범위 테스트
        test_ranges = [
            (-10000, -1000, -100, 10),  # 음수 범위
            (-2, -1, 0, 1, 2),     # 0 근처
            (10, 100, 1000, 10000),      # 양수 범위
        ]
        
        for value_range in test_ranges:
            for value in value_range:
                cap.set(prop, value)
                actual = cap.get(prop)
                if actual != current:  # 값이 변경되었을 때만 출력
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