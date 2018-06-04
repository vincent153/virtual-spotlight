import numpy as np
import cv2
import random
def gkern(l=5, sig=1.):
    """
    creates gaussian kernel with side length l and a sigma of sig
    """

    ax = np.arange(-l // 2 + 1., l // 2 + 1.)
    xx, yy = np.meshgrid(ax, ax)

    kernel = np.exp(-(xx**2 + yy**2) / (2. * sig**2))
    return kernel
    #return kernel / np.sum(kernel)

def get_spotlight(size=300):
    kernal = gkern(size,size/10)
    spotlight = np.zeros([size,size],np.uint8)
    min_p = kernal.min()
    max_p = kernal.max()
    interval = max_p-min_p
    target_min = 0
    target_max = 155
    for i in range(size):
        for j in range(size):
            value = kernal[i][j]
            newvalue = ((value-min_p)*(target_max-target_min)/interval)+target_min
            if newvalue < target_min:
                newvalue = target_min
            spotlight[i][j] = newvalue
    return spotlight

def get_rnd_start(y,x):
    y =  random.randint(0,int(y))
    x =  random.randint(0,int(x))    
    return y,x

def truncate(pix):
    if pix > 255:
        return 255
    return pix

def virtual_spotlight(img_path,spot_size=300):
    src = cv2.imread(img_path)

    if src is None:
        return

    dst = src.copy()
    spotlight = get_spotlight(spot_size)
    img_height = dst.shape[0]
    img_width = dst.shape[1]
    start_y, start_x = get_rnd_start(img_height/2,img_width/2)

    for y in range(start_y,img_height):
        for x in range(start_x,img_width):

            pixr = int(dst[y][x][2])
            pixg = int(dst[y][x][1])
            pixb = int(dst[y][x][0])

            try:
                newPixr = pixr + spotlight[y-start_y][x-start_x]
                newPixg = pixg + spotlight[y-start_y][x-start_x]
                newPixb = pixb + spotlight[y-start_y][x-start_x]
            except:
                continue

            dst[y][x][2] = truncate(newPixr)
            dst[y][x][1] = truncate(newPixg)
            dst[y][x][0] = truncate(newPixb)

    #img_spot = cv2.cvtColor(img_hsv,cv2.COLOR_HSV2BGR)
    cv2.imshow('spot',dst)
    cv2.imshow('src',src)
    cv2.waitKey()
    cv2.imwrite('out.jpg',dst)

if __name__ == '__main__': 
    import sys
    file_name = sys.argv[1]
    spot_size = int(sys.argv[2])
    virtual_spotlight(file_name, spot_size)

