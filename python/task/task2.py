import cv2
import numpy as np
import os, tkinter, tkinter.filedialog
import pathlib
import glob
from matplotlib import pyplot as plt

# 画像ファイルpathを取得
def Path():
    return tkinter.filedialog.askdirectory()

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
    cv2.floodFill(img_floodfill, mask, (0,0), 255)
    cv2.floodFill(img_floodfill, mask, (0,511), 255)
    cv2.floodFill(img_floodfill, mask, (511,0), 255)
    cv2.floodFill(img_floodfill, mask, (511,511), 255)

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
def mkFile(img_file_name,Result):
    dirname = 'Result'
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    cv2.imwrite(os.path.join(dirname, 'Result_' + img_file_name + '.jpg'), Result)

def main():
    # 画像リスト取得
    file_dir = Path()
    img_list = list(pathlib.Path(file_dir).glob('**/*.jpg'))

    for i in range(len(img_list)):
        img_dir = str(img_list[i]) # 画像Path
        img = cv2.imread(img_dir,0) # 第２引数0でグレイスケール

        # 処理
        img_th = binary(img) # 二値化
        img_fl = fillHole(img_th) # 穴埋め
        img_er = erode(img_fl) # 縮小
        img_dl = dilation(img_er) # 拡大

        Result = min_(img, img_dl) # 元画像と最小化処理
        """""
        titles = ['Original Image','BINARY','BINARY_fl','er','dl','result']
        images = [img, img_th, img_fl, img_er, img_dl, Result]

        for i in range(6):
            plt.subplot(2,3,i+1),plt.imshow(images[i],'gray')
            plt.title(titles[i])
            plt.xticks([]),plt.yticks([])
        plt.show()
        """

        cv2.imshow("Result",Result)
        cv2.waitKey(300)
        cv2.destroyAllWindows()

        img_file_name = os.path.basename(img_dir) # 画像ファイル名取得s
        mkFile(img_file_name,Result)

if __name__ == "__main__":
    main()

"""
reference : https://learnopencv.com/filling-holes-in-an-image-using-opencv-python-c/
"""