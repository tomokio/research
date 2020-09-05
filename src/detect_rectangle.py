import cv2
import numpy as np
import time

def detect_rectangle(center):

    fn = '../photo.jpg'
    flag = 0

    im = cv2.imread(fn)
    while im is None:
        im = cv2.imread(fn)

    # Switch
    time.sleep(2)

    im2 = cv2.imread(fn)
    while im2 is None:
        im2 = cv2.imread(fn)

    if im is not None and im2 is not None:
        img_diff   = cv2.absdiff(im2, im)
        img_diffm  = cv2.threshold(img_diff, 70, 255, cv2.THRESH_BINARY)[1]

        operator   = np.ones((3, 3), np.uint8)
        img_dilate = cv2.dilate(img_diffm, operator, iterations=4)
        img_mask   = cv2.erode(img_dilate, operator, iterations=4)

        img_dst    = cv2.bitwise_and(im2, img_mask)

        u_rgb1     = get_rgb(img_dst,center[2][0],center[2][1])
        u_rgb2     = get_rgb(img_dst,center[2][0],center[2][1])
        l_rgb1     = get_rgb(img_dst,center[3][0],center[3][1])
        l_rgb2     = get_rgb(img_dst,center[3][0],center[3][1])

        print("TRIANGLE:")
        print(u_rgb1)
        print(u_rgb2)
        print(l_rgb1)
        print(l_rgb2)

        if u_rgb1[0] == 128 or u_rgb1[1] == 128 or u_rgb1[2] == 128 or u_rgb2[0] == 128 or u_rgb2[1] == 128 or u_rgb2[2] == 128 \
            or l_rgb1[0] == 128 or l_rgb1[1] == 128 or l_rgb1[2] == 128 or l_rgb2[0] == 128 or l_rgb2[1] == 128 or l_rgb2[2] == 128:
            flag = 0
        else:
            if u_rgb1[0] > 0 or u_rgb2[0] > 0:    flag = 1
            elif u_rgb1[1] > 0 or u_rgb2[1] > 0:  flag = 1
            elif u_rgb1[2] > 0 or u_rgb2[2] > 0:  flag = 1
            elif l_rgb1[0] > 0 or l_rgb2[0] > 0:  flag = 2
            elif l_rgb1[1] > 0 or l_rgb2[1] > 0:  flag = 2
            elif l_rgb1[2] > 0 or l_rgb2[2] > 0:  flag = 2

        print "FLAG:%d" %flag
        print("\n")

    return flag

def get_rgb(im,cx,cy):

    try:
        rgb = im[cy, cx,:]
        tmp = rgb[0]
        rgb[0] = rgb[2]
        rgb[2] = tmp
    except TypeError:
        try:
            rgb = im[cy, cx,:]
            tmp = rgb[0]
            rgb[0] = rgb[2]
            rgb[2] = tmp
        except TypeError:
            print "cannot get rgb"

    return rgb
