import cv2

image_path = "../image to detect/mario.png"
image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

cv2.imshow("Screenshot", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
