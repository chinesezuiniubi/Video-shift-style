import cv2

# img1 = cv2.imread('1.jpeg')
# img = cv2.imwrite("D:\pycharmproject\Video_Shift_Style/1.jpg",img1)
img1 = cv2.imread('1.jpg')
res = cv2.stylization(img1, sigma_s=60, sigma_r=0.6)

cv2.imshow("sss",res)
cv2.imwrite("D:\pycharmproject\Video_Shift_Style/2.jpg",res)
cv2.waitKey(0)