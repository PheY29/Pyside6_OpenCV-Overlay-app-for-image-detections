import mss
import numpy as np
import cv2

with mss.mss() as sct:
    screenshot = np.array(sct.grab(sct.monitors[1]))[:, :, :3]  # keep h, w, (rgb)
    cv2.imshow("Screenshot", screenshot)
    cv2.waitKey(0)  # wait a key to continue program
    cv2.destroyAllWindows()  # here if a key is pressed close all screenshot
