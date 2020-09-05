import cv2
import numpy as np

def detect_circle():

    fn = '../photo.jpg'

    get_rgb1 = [0, 0, 0]
    get_rgb2 = [0, 0, 0]

    im_in    = cv2.imread(fn, 1)
    img      = cv2.imread(fn, 0)
    img      = cv2.medianBlur(img, 5)

    pt = [0, 0 ]
    step = 0

    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 10, param1 = 100, param2 = 30, minRadius = 10, maxRadius = 250)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            step = step + 1
            pt[0] = i[0]
            pt[1] = i[1]
            if step == 1:
                get_rgb1 = im_in[pt[1], pt[0], :]
            if step == 2:
                get_rgb2 = im_in[pt[1], pt[0], :]

        tmp = get_rgb1[0]
        get_rgb1[0] = get_rgb1[2]
        get_rgb1[2] = tmp
        tmp = get_rgb2[0]
        get_rgb2[0] = get_rgb2[2]
        get_rgb2[2] = tmp

    return get_rgb1
