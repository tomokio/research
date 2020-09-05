import time
import math
import random as rand

from hue import Hue
from rgb_cie import Converter
from detect_object import detect_object
from detect_object import get_rgb
from detect_rectangle import detect_rectangle

h = Hue()
h.station_ip = '172.20.11.203'
h.get_state()
l = h.lights.get('l2')
l.set_state({
    "on": True,
    "sat": 254,
    "bri": 140,
    "xy": [0.3127,0.329] # Reset to White
})


def main():

    center     = detect_object()
    target_rgb = get_pics(center)
    target_lab = convert(target_rgb)

    vled       = [127,127,127] # White
    now_rgb    = [255, 255, 255]
    now_lab    = [255, 255, 255]

    now_diff   = 1000
    bri        = 140
    control(target_rgb, bri)
    start = time.time()

    while True:

        elapsed_time = time.time() - start
        print ("Time:{:.1f}".format(elapsed_time)) + "[sec]"
        print "brightness: %d" % bri

        tmp_vled = vled
        tmp_diff = now_diff

        vled     = rand_signal(vled, now_diff)
        control(vled, bri)

        now_rgb, bri = check_color(center, bri)
        now_lab      = convert(now_rgb)
        now_diff     = (math.fabs(target_lab[0] - now_lab[0]) ** 2.0 + math.fabs(target_lab[1] - now_lab[1]) ** 2.0 + \
            math.fabs(target_lab[2] - now_lab[2]) ** 2.0) ** ( 1.0 / 2.0 )

        if now_diff > tmp_diff:
            vled     = tmp_vled
            now_diff = tmp_diff
            control(vled, bri)

        print ("Color Difference:{:.2f}".format(now_diff))

def rand_signal(vled, now_diff):

    if now_diff <= 25:
        return vled
    elif now_diff < 30:
        x = 20
    elif now_diff < 50:
        x = 30
    else:
        x = 50

    num = rand.randint(1,6)

    if num == 1:
        vled[0] += vled[0]/100 * rand.randint(0, x)
    elif num == 2:
        vled[0] += vled[0]/100 * rand.randint(-x, 0)
    elif num == 3:
        vled[1] += vled[1]/100 * rand.randint(0, x)
    elif num == 4:
        vled[1] += vled[1]/100 * rand.randint(-x, 0)
    elif num == 5:
        vled[2] += vled[2]/100 * rand.randint(0, x)
    elif num == 6:
        vled[2] += vled[2]/100 * rand.randint(-x, 0)

    vled = limit_vled(vled)

    return vled

def convert(rgb):

    xyz = [0, 0, 0]
    lab = [0, 0, 0]

    xyz[0] = (0.412391 * ((((rgb[0] / 255.0) + 0.055) / 1.055) ** 2.4) +
0.357584 * ((((rgb[1] / 255.0) + 0.055) / 1.055) ** 2.4) +
0.180481 * ((((rgb[2] / 255.0) + 0.055) / 1.055) ** 2.4)) * 100.0
    xyz[1] = (0.212639 * ((((rgb[0] / 255.0) + 0.055) / 1.055) ** 2.4) +
0.715169 * ((((rgb[1] / 255.0) + 0.055) / 1.055) ** 2.4) +
0.072192 * ((((rgb[2] / 255.0) + 0.055) / 1.055) ** 2.4)) * 100.0
    xyz[2] = (0.019331 * ((((rgb[0] / 255.0) + 0.055) / 1.055) ** 2.4) +
0.119195 * ((((rgb[1] / 255.0) + 0.055) / 1.055) ** 2.4) +
0.950532 * ((((rgb[2] / 255.0) + 0.055) / 1.055) ** 2.4)) * 100.0

    lab[0] = ( 116.0 * ((xyz[1] / 100.0)  **  ( 1.0 / 3.0 )) ) - 16.0
    lab[1] = 500.0 * ( ((xyz[0] / 95.047)  **  ( 1.0 / 3.0 )) - ((xyz[1] / 100.0)  **  ( 1.0 / 3.0 )) )
    lab[2] = 200.0 * ( ((xyz[1] / 100.0)  **  ( 1.0 / 3.0 )) -  ((xyz[2] / 108.883)  **  ( 1.0 / 3.0 )) )

    return lab

def get_pics(center):

    parts_num = 1
    rgb       = get_rgb(center,parts_num)
    return rgb

def check_color(center,bri):

    parts_num = 2
    rgb  = get_rgb(center, parts_num)
    flag = detect_rectangle(center)

    if flag == 1:
        bri += 20
    elif flag == 2:
        bri -= 20
    elif flag == 3:
        print "Adjustment Finished."

    if bri < 0 : bri = 0
    elif bri > 254 : bri=254

    return rgb, bri

def limit_vled(vled):

    for i in range(3):
        if vled[i] < 0 : vled[i] = 0
        elif vled[i] > 255 : vled[i]=255

    return vled

def control(vled, bri):

    xy = Converter().rgbToCIE1931(vled[0], vled[1], vled[2])
    l.xy(xy[0], xy[1])
    l.bri(bri)
    print('Signal sended')

if __name__ == '__main__' :main()
