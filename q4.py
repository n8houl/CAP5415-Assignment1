# Nathaniel Houlihan
# CAP 5415 - Fall 2017
# 10/2/2017
# Q4 - SUSAN Corner Detection

# Circular mask 37 pixels

"""
    PART 1 CODE
"""

def usan_alg(I, t):
    for i in range(3, len(I) - 3):
        for j in range(3, len(I[0]) - 3):
            for y in range(-3, 4):
                n = 0
                n_max = -1
                for x in range(-3, 4):
                    if y in [-3, 3] and x in [-3, -2, 2, 3]:
                        continue
                    elif y in [-2, 2] and x in [-3, 3]:
                        continue
                    else:
                        r = math.exp(-(((I[i+y][j+x] - I[i][j])/t) ** 6))
                        if r > n_max:
                            n_max = r
                        n = n + r
                g = n_max / 2
                if n >= g:
                    I[i][j] = g - n
                else:
                    I[i][j] = 0
    return I

def non_max_suppression(I, t):
    pass

    #test susan-input1.pgn
"""
    END PART 1
"""



"""
    PART 2 CODE
"""
    #test susan-input2.png
"""
    END PART 2
"""



"""
    PART 3 CODE
"""
    #call preprocessing
    #test susan-input2.png
"""
    END PART 3
"""
