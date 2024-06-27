import cv2

path = "c.png"

img = cv2.imread(path)
re_img = cv2.resize(img, dsize=(700, 700))

cv2.imshow("pic",re_img)
img_gray = cv2.cvtColor(re_img, cv2.COLOR_BGR2GRAY)

# 白黒に変換
ret, thresh = cv2.threshold(img_gray,120, 255, cv2.THRESH_BINARY_INV)
cv2.imwrite("change1.png", thresh)

# 輪郭検出
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(re_img, contours, -1, (0, 0, 255), 3)
cv2.imwrite("change2.png", re_img)

cv2.imshow("gray",img_gray)
cv2.imshow("change1",thresh)
cv2.imshow("change2",re_img)

cv2.waitKey(0)
cv2.destroyAllWindows()