# Nathaniel Houlihan
# CAP 5415 - Fall 2017
# 10/2/2017
# Q3 - Corner Detection

import matplotlib.image as img
import math

"""
    GENERAL
"""
def get_img(fname, grayscale=0):
    print("Reading in image")
    I = img.imread(fname)
    new_img = []
    for row in I:
        new_row = []
        for elem in row:
            if(grayscale == 1):
                new_row.append(int((1-elem) * 256))
            else:
                new_row.append(int((1 - elem[0]) * 256))
        new_img.append(new_row)
    return new_img

def put_img(I, fname):
    print("Writing image")
    new_img = []
    for row in I:
        new_row = []
        for i in range(len(row)):
            new_row.append([(256 - row[i])/256, (256 - row[i])/256, (256 - row[i])/256, 1.0])
        new_img.append(new_row)
    img.imsave(fname, new_img)

def fput_img(I, fname, id, ext):
    filename = "" + fname + "_" + id + "." + ext
    put_img(I, filename)

"""
    END GENERAL
"""

#Hessian Matrix
"""
    PART 1 CODE

    1.) Get derivatives for x and y directions: xx xy yy
    2.) Run eigen decomposition
    4.) Test eigenvalues for each pixel and if they are large mark the pixel as a corner
"""

# multiply poly function to multiply polynomials from eigen decomposition
def multiply_poly(p, q):
    mlist = [ [0]*o2+[i1*i2 for i1 in p]+[0]*(len(p)-o2) for o2,i2 in enumerate(q)]
    length = len(p)+len(q)-1
    res = [ sum(row[i] for row in mlist) for i in range(length)]
    return res
# determinant function for matrix with eigenvalues subtracted along diagonals
# param: m = 2x2 matrix
def det(m):
    diag_1 = multiply_poly([m[0][0], -1], [m[1][1], -1])
    diag_1[0] = diag_1[0] - m[0][1]*m[1][0]
    return diag_1

# factoring function to solve for characteristic polynomial of hessian matrix
# solves for eigenvalues
def factor(p):
    a = p[2]
    b = p[1]
    c = p[0]
    return ((-b + math.sqrt(b*b - 4 * a * c))/(2*a)), ((-b - math.sqrt(b*b - 4 * a * c))/(2*a))

def diffx(I):
    new_img = []
    for i in range(len(I) - 1):
        new_row = []
        for j in range(len(I[0]) - 1):
            new_row.append(I[i][j+1] - I[i][j])
        new_img.append(new_row)
    return new_img

def diffy(I):
    new_img = []
    for i in range(len(I) - 1):
        new_row = []
        for j in range(len(I[0]) - 1):
            new_row.append(I[i+1][j] - I[i][j])
        new_img.append(new_row)

    return new_img

def hessian_alg(I, T):
    I_x = diffx(I)
    I_xy = diffy(I_x)
    I_xx = diffx(I_x)
    I_y = diffy(I)
    I_yy = diffy(I_y)

    for i in range(len(I_xx)):
        for j in range(len(I_xx[0])):
            m = [[I_xx[i][j], I_xy[i][j]], [I_xy[i][j], I_yy[i][j]]]
            d = det(m)
            lambda1, lambda2 = factor(d)
            #print(str(lambda1) + ", " + str(lambda2))
            if(lambda1 > T or lambda2 > T):
                I[i][j] = 255
    return I

"""
    END PART 1 CODE
"""

#HARRIS
"""
Process:
    1.) compute horizontal and vertical derivatives of image (convolve with derivative of Gaussian)
    2.) Compute outer products of gradients M
    3.) Convolve with larger gaussian
    4.) Compute scalar interest measure R
    5.) Find local maxima above threshold t, detect corners
"""

"""
    PART 2 CODE
"""

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

def harris_alg(I, T, alpha=float(1/25)):
    xmask, ymask = gaussian_mask(3)
    L_x, L_y = convolute(I, xmask, ymask)
    L_xx = diffx(L_x)
    L_xy = diffy(L_x)
    L_yy = diffy(L_y)

    for i in range(len(L_xx)):
        for j in range(len(L_xx[0])):
            h = [[L_xx[i][j], L_xy[i][j]], [L_xy[i][j], L_yy[i][j]]]
            determinant = h[0][0]*h[1][1] - h[0][1]*h[1][0]
            trace = h[0][0] + h[1][1]
            cornerness = determinant - alpha*trace
            if(cornerness > T):
                I[i][j] = 255
    return I

def harris_alg_alt(I, T, alpha=float(1/25)):
    xmask, ymask = gaussian_mask(3)
    L_x, L_y = convolute(I, xmask, ymask)
    L_xx = diffx(L_x)
    L_xy = diffy(L_x)
    L_yy = diffy(L_y)

    for i in range(len(L_xx)):
        for j in range(len(L_xx[0])):
            h = [[L_xx[i][j], L_xy[i][j]], [L_xy[i][j], L_yy[i][j]]]

            d = det(h)
            lambda1, lambda2 = factor(d)

            cornerness = lambda1*lambda2 - alpha*(lambda1 + lambda2)
            if(cornerness > T):
                I[i][j] = 255
    return I

"""
    END PART 2
"""
# Hessian code
I = get_img('img/input2.png')
I_hess = hessian_alg(I, 75)
put_img(I_hess, 'img/q3/input2_hess.png')

# Harris pt 1 code

I = get_img('img/input2.png')
I_harris = harris_alg(I, 10)
put_img(I_harris, 'img/q3/input2_harris.png')

# Harris pt 2 code

I = get_img('img/input2.png')
I_harris_alt = harris_alg_alt(I, 10)
put_img(I_harris_alt, 'img/q3/input2_harris_alt.png')
