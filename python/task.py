import cv2
import numpy as np
from matplotlib import pyplot as plt
import os, tkinter, tkinter.filedialog, tkinter.messagebox

def __Path():
    # ファイル選択ダイアログの表示
    root = tkinter.Tk()
    root.withdraw()
    fTyp = [("","*")]
    iDir = os.path.abspath(os.path.dirname(__file__))
    tkinter.messagebox.showinfo('File','Select Image File')
    return tkinter.filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)

def binary(img):
    # グレイスケール
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 白黒に変換
    ret,thresh = cv2.threshold(img_gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    return thresh

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

def erode(im_fill):
    kernel = np.ones((5,5),np.uint8)
    erosion = cv2.erode(im_fill,kernel,iterations = 2)
    return erosion

def dilation(im_er):
    kernel = np.ones((5,5),np.uint8)
    dilation = cv2.dilate(im_er,kernel,iterations = 2)
    return dilation


def invert(im_er):
    return cv2.bitwise_not(im_er)

def main():
    path = __Path()
    img = cv2.imread(path)

    im_th = binary(img)
    im_fl = fillhole(im_th)
    im_er = erode(im_fl)
    im_dl = dilation(im_er)
    # RGBに拡張
    binary_image_colored = cv2.cvtColor(im_dl, cv2.COLOR_GRAY2BGR)
    im_min = cv2.min(img, binary_image_colored)

    titles = ['Original','Binary','Fillhole','Erode','Dilation','Result']
    images = [img, im_th, im_fl, im_er, im_dl, im_min]

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