import mss
import numpy as np
import cv2

image_path = "image to detect/mario.png"
image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

scales = np.arange(0.1, 1, 0.1)

with mss.mss() as sct:
    screenshot = np.array(sct.grab(sct.monitors[1]))[:, :, :3]  # keep h, w, (rgb)
    screenshot = screenshot.astype(np.uint8)

    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    for scale in scales:
        resized_image = cv2.resize(image, (0, 0), fx=scale, fy=scale)
        template_gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

        result = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        threshold = 0.7
        if max_val >= threshold:
            top_left = max_loc
            bottom_right = (top_left[0] + resized_image.shape[1], top_left[1] + resized_image.shape[0])

            cv2.rectangle(screenshot, top_left, bottom_right, (0, 0, 255), 2)

cv2.imshow("Detected", screenshot)
cv2.waitKey(0)
cv2.destroyAllWindows()
