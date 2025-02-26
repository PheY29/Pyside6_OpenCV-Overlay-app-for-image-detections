import mss
import numpy as np
import cv2

image_path = "../image to detect/mario.png"
image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

with mss.mss() as sct:
    screenshot = np.array(sct.grab(sct.monitors[1]))[:, :, :3]  # keep h, w, (rgb)
    screenshot = screenshot.astype(np.uint8)
    cv2.imshow("Screenshot", screenshot)
    cv2.waitKey(0)  # wait a key to continue program
    cv2.destroyAllWindows()  # here if a key is pressed close all screenshot

screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
template_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

result = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
threshold = 0.7
loc = np.where(result >= threshold)

for pt in zip(*loc[::-1]):
    top_left = pt[0] - 30, pt[1] - 30
    bottom_right = pt[0] + image.shape[1] + 30, pt[1] + image.shape[0] + 70

    cv2.rectangle(screenshot, top_left, bottom_right, (0, 0, 255), 1)

cv2.imshow("Detected", screenshot)
cv2.waitKey(0)
cv2.destroyAllWindows()
