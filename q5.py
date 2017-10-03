# Nathaniel Houlihan
# CAP 5415 - Fall 2017
# 10/2/2017
# Q5 - Processing Grayscale Images`
import matplotlib.pyplot as plt
import matplotlib.image as img
import numpy as np
"""
    GENERAL
        - Functions for reading / writing image using matplotlib
        - Manual conversion from rgb to grayscale being performed
"""
def get_img(fname):
    print("Reading in image")
    I = img.imread(fname)
    new_img = []
    for row in I:
        new_row = []
        for elem in row:
            new_row.append(elem)
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


"""
    END PART 2 CODE
"""


"""
    Running code
"""
#PART 1
I = get_img('img/moo2.png')
I = quantize_img(I)
plot_hist(I)
I = hist_eq(I)
plot_hist(I)

put_img(I, 'img/q5/moo2.png')

#PART 2
