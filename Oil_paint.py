import cv2
import numpy as np

img_oil = cv2.imread('123.jpeg')
res = cv2.xphoto.oilPainting(img_oil, 5, 1)
ret = cv2.xphoto.oilPainting(img_oil, 6, 1)
imgs = np.hstack([res,ret])
cv2.imshow('RESULT',imgs)

cv2.waitKey(0)
