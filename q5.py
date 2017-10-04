# Nathaniel Houlihan
# CAP 5415 - Fall 2017
# 10/2/2017
# Q5 - Processing Grayscale Images`
import matplotlib.pyplot as plt
import matplotlib.image as img
import numpy as np

import math
"""
    GENERAL
        - Functions for reading / writing image using matplotlib
        - Manual conversion from rgb to grayscale being performed
"""
def get_img(fname, grayscale=0):
    print("Reading in image")
    I = img.imread(fname)
    new_img = []
    for row in I:
        new_row = []
        for elem in row:
            if(grayscale == 1):
                new_row.append(elem)
            else:
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

def fput_img(I, fname, id, ext):
    filename = "" + fname + "_" + id + "." + ext
    put_img(I, filename)

"""
    END GENERAL
"""



"""
    PART 1 CODE
"""
# Generate histogram for Image I
def gen_hist(I):
    print("Generating histogram")
    hist = [0] * 256
    for i in range(len(I)):
        for j in range(len(I[0])):
            hist[I[i][j]] = hist[I[i][j]] + 1
    return hist



# Run histogram equalization on Image I
def hist_eq(I):
    print("Running histogram equalization")
    #quantize image
    max = 0
    I = quantize_img(I)
    hist = gen_hist(I)

    # get probability for each pixel
    p = [0] * 256
    for i in range(len(p)):
        p[i] = hist[i] / (len(I)*len(I[0]))

    cp = [0] * 256
    cp_sum = 0
    for i in range(len(p)):
        cp_sum = cp_sum + p[i]
        if cp_sum > 1:
            cp_sum = 1
        cp[i] = cp_sum
    new_img = I
    for i in range(len(I)):
        for j in range(len(I[0])):
            new_img[i][j] = (int(255 * cp[I[i][j]]))

    return new_img


# Plot the histogram using matplotlib module
def plot_hist(I):
    print("Plotting histogram")
    pix_vals = [i for i in range(256)]
    hist = gen_hist(I)
    plt.bar(pix_vals, hist)
    plt.show()


# Transform image from being float intensity values to being integer intensity values
# from 0 - 255 inclusive
def quantize_img(I):
    print("Quantizing image")
    max = 0
    for i in range(len(I)):
        for j in range(len(I[0])):
            if I[i][j] > max:
                max = I[i][j]
    for i in range(len(I)):
        for j in range(len(I[0])):
            I[i][j] = int((I[i][j] / max) * 255)
    return I
"""
    END PART 1 CODE
"""


"""
    PART 2 CODE
"""
# greyscale clipping function
def clipVFunction(i, a, b, beta):
    ret = -1
    if i < a and i >= 0:
        ret = 0
    elif i < b and i >= a:
        ret = beta * (i - a)
    else:
        ret = beta * (b - a)
    return ret

#perform clipping operation on each pixel in image
def clip(I, a, b, beta):
    print("Performing clipping gradation")
    I = quantize_img(I)
    new_img = I
    print("Applying clip function")
    for i in range(len(I)):
        for j in range(len(I[0])):
            new_img[i][j] = clipVFunction(I[i][j], a, b, beta)
    return new_img

"""
    END PART 2 CODE
"""


"""
    PART 3 CODE
"""
def rangeCompressionFunction(i, c):
    return c * math.log10(1 + i)

def rangeCompression(I, c):
    print("Performing log10 range compression with c=%d" % c)
    I = quantize_img(I)
    new_img = I
    print("Applying log10 range compression function")
    for i in range(len(I)):
        for j in range(len(I[0])):
            new_img[i][j] = rangeCompressionFunction(I[i][j], c)

    return new_img

"""
    END PART 3 CODE
"""


"""
    Running code
"""
#PART 1
I = get_img('img/moo2.png', grayscale=1)
I = quantize_img(I)
plot_hist(I)
I = hist_eq(I)
plot_hist(I)

put_img(I, 'img/q5/moo2_eq.png')

#PART 2
# this is all set up, just need to find a good image to use it on
I = get_img('img/input3.png')
I = clip(I, 50, 150, 2)
put_img(I, 'img/q5/input3_clipped.png')

#PART 3
c_values = [1, 10, 100, 1000]
I = get_img('img/input3.png')
for value in c_values:
    img1 = rangeCompression(I, value)
    fput_img(img1, 'img/q5/input3', '%d' % value, 'png')
