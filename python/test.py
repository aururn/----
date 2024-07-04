import cv2

# 画像読み込み
path = r"C:\Users\Aurum\Documents\img\test.jpg"
img = cv2.imread(path)

#re_img = cv2.resize(img, dsize=(700, 700))
cv2.imshow("pic",img)

# グレイスケール
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 白黒に変換
ret, thresh = cv2.threshold(img_gray, 0, 255, cv2.THRESH_OTSU)

#閾値がいくつになったか確認
print("ret1: {}".format(ret))


# 輪郭検出
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(img, contours, -1, (255, 0, 0), 2)

cv2.imshow("gray",img_gray)
cv2.imshow("binary",thresh)
cv2.imshow("contour",img)

cv2.waitKey(0)
cv2.destroyAllWindows()