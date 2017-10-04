# Nathaniel Houlihan
# CAP 5415 - Fall 2017
# 10/2/2017
# Q2 - Entropy for Thresholding

import matplotlib.pyplot as plt
import matplotlib.image as img

import math

"""
    GENERAL
        - Functions for reading / writing image using matplotlib
        - Manual conversion from rgb to grayscale being performed
"""
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

def gen_hist(I):
    print("Generating histogram")
    hist = [0] * 256
    for i in range(len(I)):
        for j in range(len(I[0])):
            hist[I[i][j]] = hist[I[i][j]] + 1
    return hist

# Plot the histogram using matplotlib module
def plot_hist(I):
    print("Plotting histogram")
    pix_vals = [i for i in range(256)]
    hist = gen_hist(I)
    plt.bar(pix_vals, hist)
    plt.show()

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
    return quantize_img(new_img)

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

def eFunc(x):
    summation = 0
    #print(x)
    for i in range(1, len(x)):
        if x[i] > 0:
            summation += (x[i] * math.log10(x[i]))
    return -summation

def p(i, hist, N):
    if hist[i] == 0:
        return 0
    return hist[i]/N

#Entropy formulation is wrong
#figure this out later
def sumEntropies(I):
    I = quantize_img(I)

    N = len(I)*len(I[0])

    max_entropy = -1
    max_entropy_thresh = -1
    hist = gen_hist(I)

    starting_thresh = next((i for i, x in enumerate(hist) if x), None)
    ending_thresh = len(hist) - next((i for i, x in enumerate(reversed(hist)) if x), None)

    print(ending_thresh)


    threshs = [i for i in range(starting_thresh, ending_thresh)]
    for T in threshs:
        PT = hist[T] / N
        #
        A = [p(i, hist, N)/p(T, hist, N) for i in range(1, T+1)]
        B = [p(i, hist, N)/(1-p(T, hist, N)) for i in range(T+1, len(threshs))]

        total_entropy = eFunc(A) + eFunc(B)

        if total_entropy < max_entropy:
            max_entropy_thresh = T
            max_entropy = total_entropy

    return max_entropy_thresh

I = get_img('img/coins.png', grayscale=1)
plot_hist(I)
optimum_thresh = sumEntropies(I)

new_img = I
for i in range(len(I)):
    for j in range(len(I[0])):
        if I[i][j] >= optimum_thresh:
            new_img[i][j] = 1.0
        else:
            new_img[i][j] = 0
print(optimum_thresh)
put_img(I, 'img/q2/coins_entropythresh.png')
