# Nathaniel Houlihan
# CAP 5415 - Fall 2017
# 10/2/2017
# Q3 - Corner Detection

#HARRIS
"""
Process:
    1.) compute horizontal and vertical derivatives of image (convolve with derivative of Gaussian)
    2.) Compute outer products of gradients M
    3.) Convolve with larger gaussian
    4.) Compute scalar interest measure R
    5.) Find local maxima above threshold t, detect corners
"""
