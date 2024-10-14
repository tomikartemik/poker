# src/image_processing.py

import cv2
import pytesseract

def process_image(img):
    """Обработка изображения для распознавания текста"""
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray_img)
    return text
