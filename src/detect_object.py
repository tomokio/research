import cv2
import numpy as np

def detect_object():

    # about parts_num
    # 1=coloring part, 2=marker, 3,4=illuminance control parts

    # file path
    fn = '../photo.jpg'

    # input image
    photo = cv2.imread(fn,cv2.IMREAD_COLOR)

    # gray scale
    gray = cv2.cvtColor(photo, cv2.COLOR_BGR2GRAY)

    # edge detection
    edge = cv2.Canny(gray,5,45) # This setting can recognize most of UIs.

    # binarization
    bw = cv2.adaptiveThreshold(edge,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)

    # bit inversion
    bw_inv = cv2.bitwise_not(bw)

    # find contours
    _, contours, _ = cv2.findContours(bw_inv,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    rects = []
    detect_count = 0

    # for each contours
    for i in range(0, len(contours)):
        area = cv2.contourArea(contours[i])
        if area < 1e3 or 1e5 < area:
            continue

        if len(contours[i]) > 0:
            # calculate bounding rectangles
            rect = cv2.boundingRect(contours[i])
            rect = list(rect)
            rects.append(rect)
            # write rectangles
            x, y, w, h = cv2.boundingRect(contours[i])
            cv2.rectangle(photo, (x, y), (x + w, y + h), (0, 255, 0), 2)
        detect_count = detect_count + 1

    if detect_count < 4:
        print('Error: Too little objects.')
        exit()

    # correct rectangles
    if detect_count > 4:
        area = []
        # sort rectangles by area size
        for i in range(0, detect_count):
            x, y, w, h = rects[i]
            area.append(w*h)
        for i in range(0, detect_count):
            max_num = area.index(max(area))
            rects[i], rects[max_num] = rects[max_num], rects[i]
            area[max_num] = 0
            area[i], area[max_num] = area[max_num], area[i]
        # for intersected and adjoined rectangles
        for i in range(0, 4):
            x1, y1, w1, h1 = rects[i]
            for j in range(i+1, detect_count):
                x2, y2, w2, h2 = rects[j]
                if(((x1 < x2+w2) and (x1+w1 > x2) and (y1 < y2+h2) and (y1+h1 > y2)) or \
                ((x1+w1 == x2) or (x2+w2 == x1) or (y1+h1 == y2) or (y2+h2 == y1))):
                    if(min(x1, x2) == x2):
                        w1 = w1+(x1-x2)
                        x1 = x2
                        rects[i] = (x1, y1, w1, h1)
                    elif(max(x1+w1, x2+w2) == x2+w2):
                        w1 = (x2+w2)-x1
                        rects[i] = (x1, y1, w1, h1)
                    elif(min(y1, y2) == y2):
                        h1 = h1+(y1-y2)
                        y1 = y2
                        rects[i] = (x1, y1, w1, h1)
                    elif(max(y1+h1, y2+h2) == y2+h2):
                        h1 = (y2+h2)-y1
                        rects[i] = (x1, y1, w1, h1)
                    # write corrected rectangles
                    cv2.rectangle(photo, (x1, y1), (x1 + w1, y1 + h1), (0,0,255), 2)

    # save photo of corrected rectangles
    cv2.imwrite('../results/detected_objects_1.jpg' ,photo)

    # find center coordinates
    center = []
    for i in range(0, 4):
        x, y, w, h = rects[i]
        cx = x+w/2
        cy = y+h/2
        center.append([cx, cy])

    # sort objects
    center.sort(reverse=True)
    if sum(center[0]) > sum(center[1]):
        tmp = center[0]
        center[0] = center[1]
        center[1] = tmp
    if sum(center[2]) > sum(center[3]):
        tmp = center[2]
        center[2] = center[3]
        center[3] = tmp
    center = np.array(center)

    # check center coordinates
    for i in range(1, 4):
        # if pixel value is 0(=black)
        if bw[center[i][1], center[i][0]] == 0:
            y = center[i][1]-5
            x = center[i][0]-5
            width = 10
            value = 0
            # get pixel value of neighborhood pixels
            while value == 0:
                y = y-1
                x = x-1
                width = width+2
                value = bw[y, x]
                # x++
                for j in range(1, width+1):
                    if value == 255: break
                    x = x+1
                    value = bw[y, x]
                # y++
                for j in range(1, width+1):
                    if value == 255: break
                    y = y+1
                    value = bw[y, x]
                # x--
                for j in range(1, width+1):
                    if value == 255: break
                    x = x-1
                    value = bw[y, x]
                # y--
                for j in range(1, width+1):
                    if value == 255: break
                    y = y-1
                    value = bw[y, x]
            # replace coordinates
            print photo[center[i][1], center[i][0]]
            cv2.circle(photo,(center[i][0],center[i][1]),2,(0,0,0),5)
            center[i][1] = y
            center[i][0] = x
            print photo[center[i][1], center[i][0]]
            print photo[320,240]

    # print results
    cv2.circle(photo,(center[0][0],center[0][1]),2,(0,0,255),5) # color
    cv2.circle(photo,(center[1][0],center[1][1]),2,(255,0,0),5) # check
    cv2.circle(photo,(center[2][0],center[2][1]),2,(0,255,255),5) # up
    cv2.circle(photo,(center[3][0],center[3][1]),2,(255,255,255),5) # down
    print 'contours:', detect_count

    cv2.imwrite('../results/detected_objects_2.jpg' ,photo)

    return center

def get_rgb(center,parts_num):

    # file path
    fn = '../photo.jpg'

    # input image
    photo = cv2.imread(fn,cv2.IMREAD_COLOR)
    while photo is None:
        photo = cv2.imread(fn,cv2.IMREAD_COLOR)

    if parts_num==1:
        rgb = photo[center[0][1], center[0][0]]
        tmp_rgb = rgb[0]
        rgb[0] = rgb[2]
        rgb[2] = tmp_rgb
        return rgb

    elif parts_num==2:
        rgb = photo[center[1][1], center[1][0]]
        tmp_rgb = rgb[0]
        rgb[0] = rgb[2]
        rgb[2] = tmp_rgb
        return rgb

    elif parts_num==3:
        rgb = photo[center[2][1], center[2][0]]
        tmp_rgb = rgb[0]
        rgb[0] = rgb[2]
        rgb[2] = tmp_rgb
        return rgb

    elif parts_num==4:
        rgb = photo[center[3][1], center[3][0]]
        tmp_rgb = rgb[0]
        rgb[0] = rgb[2]
        rgb[2] = tmp_rgb
        return rgb


if __name__ == '__main__': detect_object()
