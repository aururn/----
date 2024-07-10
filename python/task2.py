import cv2
import numpy as np
from matplotlib import pyplot as plt
import os, tkinter, tkinter.filedialog, tkinter.messagebox

# 画像ファイル取得
def __Path():
    root = tkinter.Tk()
    root.withdraw()
    fTyp = [("","*")]
    iDir = os.path.abspath(os.path.dirname(__file__))
    return tkinter.filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)

# 二値化処理
def binary(img):
    # グレイスケール
    # img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 白黒に変換
    ret,thresh = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    return thresh

# 穴埋め
def fillhole(im_th):

    im_floodfill = im_th.copy()

    h, w = im_th.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)

    # Floodfill from point (0, 0)
    cv2.floodFill(im_floodfill, mask, (0,0), 255);

    # Invert floodfilled image
    im_floodfill_inv = cv2.bitwise_not(im_floodfill)
    im_out = im_th | im_floodfill_inv
    return im_out

# 画像縮小
def erode(im_fill):
    kernel = np.ones((5,5),np.uint8)
    erosion = cv2.erode(im_fill,kernel,iterations = 2)
    return erosion

# 画像拡大
def dilation(im_er):
    kernel = np.ones((5,5),np.uint8)
    dilation = cv2.dilate(im_er,kernel,iterations = 2)
    return dilation


def invert(im_er):
    return cv2.bitwise_not(im_er)

def main():
    # 画像読み込み
    path = __Path()
    img = cv2.imread(path,0) # 引数0:グレイスケール

    im_th = binary(img) # 二値化画像
    im_fl = fillhole(im_th) # 穴埋め画像
    im_er = erode(im_fl) # 穴埋め画像の縮小
    im_dl = dilation(im_er) # 縮小画像の拡大 (ベットを削除)
    im_inv = invert(im_th) # 二値化画像の反転

    im_and = cv2.bitwise_and(im_inv, im_dl) # 反転画像と拡大画像でAND処理

    # RGBに拡張
    #binary_image_colored = cv2.cvtColor(im_and, cv2.COLOR_GRAY2BGR)
    im_min = cv2.min(img, im_and) # 元画像とAND処理画像の最小値

    titles = ['Original','Binary','FillHole','Erode','Dilation','And']
    images = [img, im_th, im_fl, im_er, im_dl, im_and]

    n = len(titles)
    row = 2 # 列
    col = 3 # 行
    for i in range(n):
        plt.subplot(row,col,i+1),plt.imshow(images[i],'gray')
        plt.title(titles[i])
        plt.xticks([]),plt.yticks([])

    cv2.imshow('Original',img)
    cv2.imshow('Result',im_min)

    plt.show()
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

"""
reference : https://learnopencv.com/filling-holes-in-an-image-using-opencv-python-c/
"""