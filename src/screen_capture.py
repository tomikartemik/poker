# src/screen_capture.py

import mss
import cv2
import numpy as np
from config import REGION_TABLE

def capture_screen(region=REGION_TABLE):
    """Функция для захвата экрана в заданной области"""
    with mss.mss() as sct:
        screenshot = sct.grab(region)
        img = np.array(screenshot)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        cv2.imshow("Captured Screen", img)  # Показать захваченную область экрана
        cv2.waitKey(0)  # Ожидать нажатия клавиши, чтобы закрыть окно
        cv2.destroyAllWindows()
        return img
