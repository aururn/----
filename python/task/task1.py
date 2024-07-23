import cv2
import numpy as np
import os, tkinter, tkinter.filedialog

# 画像ファイル取得
def Path_():
    return tkinter.filedialog.askopenfilename()

# 二値化処理
def binary(img):

    ret,thresh = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    # 閾値確認
    print("threshold Value: {}".format(ret))

    return thresh

# 穴埋め処理
def fillHole(img):

    img_floodfill = img.copy()

    # マスク処理
    h, w = img.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)

    # 穴埋め
    # print(img.shape) -> (512,512)
    cv2.floodFill(img_floodfill, mask, (0,0), 255);
    cv2.floodFill(img_floodfill, mask, (0,511), 255);
    cv2.floodFill(img_floodfill, mask, (511,0), 255);
    cv2.floodFill(img_floodfill, mask, (511,511), 255);

    # 反転処理
    img_floodfill_inv = invert(img_floodfill)
    img_out = or_(img,img_floodfill_inv)

    return img_out

    """""
    contours,_ = cv2.findContours(img,1,2)
    fillHole = np.zeros(img.shape, dtype="uint8")
    for p in contours:
        cv2.fillPoly(fillHole,[p],(255,255,255))
    return fillHole
    """

# 画像縮小処理
def erode(img):
    kernel = np.ones((5,5),np.uint8)

    return cv2.erode(img,kernel,iterations = 2)

# 画像拡大処理
def dilation(img):
    kernel = np.ones((5,5),np.uint8)

    return cv2.dilate(img,kernel,iterations = 2)

# 反転処理
def invert(img):
    return cv2.bitwise_not(img)

# 最小化処理
def min_(img1,img2):
    return cv2.min(img1,img2)

# and処理
def and_(img1,img2):
    return cv2.bitwise_and(img1, img2)

# or処理
def or_(img1,img2):
    return cv2.bitwise_or(img1, img2)

# 保存場所作成
def mkFile(Result):
    dirname = 'Result'
    if not os.path.exists(dirname):
        os.mkdir(dirname)

    cv2.imwrite(os.path.join(dirname, 'Result.jpg'), Result)

def main():
    # 画像取得
    img_path = Path_()
    img = cv2.imread(img_path,0)

    # 処理
    img_th = binary(img) # 二値化
    img_fl = fillHole(img_th) # 穴埋め
    img_er = erode(img_fl) # 縮小
    img_dl = dilation(img_er) # 拡大

    Result = min_(img, img_dl) # 元画像と最小化処理

    mkFile(Result)

if __name__ == "__main__":
    main()

"""
references : https://learnopencv.com/filling-holes-in-an-image-using-opencv-python-c/
"""