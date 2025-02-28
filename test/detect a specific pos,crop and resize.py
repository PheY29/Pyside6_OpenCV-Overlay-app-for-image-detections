import mss
import cv2
import numpy as np

crop_x, crop_y, crop_width, crop_height = 500, 500, 500, 200

with mss.mss() as sct:
    screenshot = np.array(sct.grab(sct.monitors[1]))[:, :, :3]
    cropped_img = screenshot[crop_y:crop_y + crop_height, crop_x:crop_x + crop_width]  # [start:end, start:end]


cv2.imshow("Image", cropped_img)
cv2.waitKey(0)
cv2.destroyAllWindows()


scale_factor = 3
resized_img = cv2.resize(cropped_img, (crop_width * scale_factor, crop_height * scale_factor),
                         interpolation=cv2.INTER_LINEAR)

# gray = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)
# _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)  # _ = thresh_value = 150

cv2.imshow("Image", resized_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
