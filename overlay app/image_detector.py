import sys
import mss
import numpy as np
import cv2

from PySide6.QtGui import QIcon, QAction, QPainter, QColor, QPen
from PySide6.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QSystemTrayIcon, QMenu
from PySide6.QtCore import Qt, QTimer


img_path = "image to detect/mario.png"
image = (cv2.imread(img_path, cv2.IMREAD_UNCHANGED))


class Overlay(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(0, 0, 1920, 1080)  # x, y, w, h

        self.detections = []

    def setup_ui(self):
        self.create_layouts()
        self.create_system_tray()

    def create_layouts(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QLabel(self.central_widget)

    def create_system_tray(self):
        self.systray_icon = QSystemTrayIcon(self)
        self.systray_icon.setIcon(QIcon("icon/mario.png"))
        self.systray_menu = QMenu()

        self.quit_action = QAction("Exit", self)
        self.quit_action.triggered.connect(self.quit_app)
        self.systray_menu.addAction(self.quit_action)

        self.systray_icon.setContextMenu(self.systray_menu)
        self.systray_icon.show()

    def quit_app(self):
        self.systray_icon.hide()
        QApplication.quit()

    def update_detections(self, detections):
        self.detections = detections
        self.repaint()  # call paintEvent

    def paintEvent(self, event):
        """
        draw rect on target
        :param event: obtain automatically coordinate on where draw
        :return: new position of rectangle
        """
        painter = QPainter(self)
        pen_width = 3
        painter.setPen(QPen(QColor(255, 0, 0, 200), pen_width))

        for x, y in self.detections:
            painter.drawRect(x, y, image.shape[1], image.shape[0])


app = QApplication(sys.argv)
overlay = Overlay()
overlay.show()


def detect_image():
    with mss.mss() as sct:
        screenshot = np.array(sct.grab(sct.monitors[1]))[:, :, :3]
        screenshot = screenshot.astype(np.uint8)

        screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        template_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        result = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(result >= threshold)

        detections = list(zip(*loc[::-1]))
        overlay.update_detections(detections)

        del screenshot
        del detections


timer = QTimer()
timer.timeout.connect(detect_image)
timer.start(50)

sys.exit(app.exec())
