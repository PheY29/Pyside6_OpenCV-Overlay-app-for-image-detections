import sys
import mss
import cv2
import numpy as np
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer


def screen_is_black(screenshot, threshold=10):
    gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    brightness = np.mean(gray)
    result = bool(brightness < threshold)
    return result


def detect():
    crop_x, crop_y, crop_width, crop_height = 700, 300, 250, 250

    with mss.mss() as sct:
        screenshot = np.array(sct.grab(sct.monitors[1]))[:, :, :3]
        cropped_img = screenshot[crop_y:crop_y + crop_height, crop_x:crop_x + crop_width]

        if screen_is_black(cropped_img):
            print("black screen detected")


app = QApplication(sys.argv)

timer = QTimer()
timer.timeout.connect(detect)
timer.start(50)

app.exec()
