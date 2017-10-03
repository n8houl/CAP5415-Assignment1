# Nathaniel Houlihan
# CAP 5415 - Fall 2017
# 10/2/2017
# Q1 - Canny Edge Detection

"""
    TODO:
        Comment then done
            optional: add the x and y smoothing intermediary images
"""
import math
import matplotlib.image as img


def gaussian_mask(size, sigma=1.5):
    print("Generating gauss mask")
    maskx = []
    masky = []
    for p in range(-int(size/2), int(size/2) + 1):
        x_row = []
        y_row = []
        for q in range(-int(size/2), int(size/2) + 1):
            maskval = q * math.exp(-1 * ((p*p + q*q)/(2 * sigma * sigma)))
            x_row.append(maskval)
            maskval = p * math.exp(-1 * ((p*p + q*q)/(2 * sigma * sigma)))
            y_row.append(maskval)
        maskx.append(x_row)
        masky.append(y_row)
    return maskx, masky
def get_img(fname):
    print("Reading in image")
    I = img.imread(fname)
    new_img = []
    for row in I:
        new_row = []
        for elem in row:
            new_row.append(elem[0])
        new_img.append(new_row)
    return new_img

def put_img(I, fname):
    print("Writing image")
    new_img = []
    for row in I:
        new_row = []
        for i in range(len(row)):
            new_row.append([row[i], row[i], row[i], 1.0])
        new_img.append(new_row)
    img.imsave(fname, new_img)

def convolute(I, kx, ky):
    print("Performing convolution")
    conv1 = []
    conv2 = []

    mr = int(len(kx)/2)
    I_h = len(I)
    I_w = len(I[0])

    for i in range(mr, I_h - mr):
        row_c1 = []
        row_c2 = []
        for j in range(mr, I_w - mr):
            s1 = 0
            s2 = 0
            for p in range(-mr, mr + 1):
                for q in range(-mr, mr + 1):
                    s1 += I[i + p][j + q] * kx[p + mr][q + mr]
                    s2 += I[i + p][j + q] * ky[p + mr][q + mr]
            row_c1.append(s1)
            row_c2.append(s2)
        conv1.append(row_c1)
        conv2.append(row_c2)
    return conv1, conv2

def magnitude(C1, C2, k):
    print("Generating magnitude image")
    ival = []
    maxival = 0
    mr = int(len(k)/2)
    C1_h = len(C1)
    C1_w = len(C1[0])
    for i in range(mr, (C1_h - mr) + 1):
        ival_row = []
        for j in range(mr, (C1_w - mr) + 1):
            val = math.sqrt((C1[i][j]*C1[i][j]) + (C2[i][j]*C2[i][j]))
            ival_row.append(val)
            if val > maxival:
                maxival = val
        ival.append(ival_row)
    for i in range(len(ival)):
        for j in range(len(ival[0])):
            ival[i][j] = ival[i][j] / maxival
    return ival

def peaks(C1, C2, ival, k):
    print("Generating peaks image")
    peaks = [[0] * len(C1[0]) for _ in range(len(C1))]
    mr = int(len(k) / 2)
    for i in range(mr, len(C1) - mr - 1):
        for j in range(mr, len(C1[0])-mr - 1):
            if(C1[i][j] == 0):
                C1[i][j] = 0.00001;

            tandir = C2[i][j] / C1[i][j]
            if tandir <= math.tan((22.5 * math.pi)/180.0) and tandir > math.tan((-22.5 * math.pi)/180.0):
                if(ival[i][j] > ival[i][j-1] and ival[i][j] > ival[i][j+1]):
                    peaks[i][j] = 1.0
            elif tandir <= math.tan((67.5 * math.pi)/180.0) and tandir > math.tan((22.5 * math.pi)/180.0):
                if(ival[i][j] > ival[i-1][j-1] and ival[i][j] > ival[i+1][j+1]):
                    peaks[i][j] = 1.0
            elif tandir <= math.tan((-22.5 * math.pi)/180.0) and tandir > math.tan((-67.5 * math.pi)/180.0):
                if(ival[i][j] > ival[i+1][j-1] and ival[i][j] > ival[i-1][j+1]):
                    peaks[i][j] = 1.0
            else:
                if(ival[i][j] > ival[i-1][j] and ival[i][j] > ival[i+1][j]):
                    peaks[i][j] = 1.0
    return peaks

def thresh(ival, peaks, hi, lo):
    print("Performing hysteresis thresholding")
    final = [[0] * len(ival[0]) for _ in range(len(ival))]
    for i in range(len(ival)):
        for j in range(len(ival[0])):
            if ival[i][j] > hi:
                final[i][j] = 1.0
            else:
                final[i][j] = 0

    moretodo = 1
    while not (moretodo == 0):
        moretodo = 0
        for i in range(len(ival)):
            for j in range(len(ival[0])):
                if peaks[i][j] > 0:
                    for p in range(-1, 2):
                        for q in range(-1, 2):
                            if final[i+p][j+q] > 0:
                                peaks[i][j] = 0
                                final[i][j] = 1.0
                                moretodo = 1
    return final

def detect_edges(filename):
    filename = filename.split('.')[0]
    I = get_img('%s.png' % filename)
    kx, ky = gaussian_mask(3)
    C1, C2 = convolute(I, kx, ky)
    put_img(C1, '%s_xdir.png' % filename)
    put_img(C2, '%s_ydir.png' % filename)
    ival = magnitude(C1, C2, kx)
    put_img(ival, '%s_mag.png' % filename)
    peaks_img = peaks(C1, C2, ival, kx)
    final = thresh(ival, peaks_img, .3, .6)
    put_img(final, '%s_final.png' % filename)

detect_edges('img/input3.png')
