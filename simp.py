# Extended Simpson's rule (and other variants)

def quad(xvar, yvar, ifix, ind):

    h = xvar[1] - xvar[0]; li = ifix; ui = ifix + ind # step size; lower index; upper index
    while (ui > (len(xvar) - 1)):
        ui -= 1
    n = len(xvar[li:ui])

    if (n == 0):
        raise ValueError('Not enough data points')
        exit()
    elif (n == 1): # Trapezoid rule
        quad = (xvar[ui] - xvar[li]) * (yvar[li + 1] + yvar[li]) / 2
        return quad
        exit()
    elif (n == 2): # Simpson's rule
        quad = (xvar[ui] - xvar[li]) * (yvar[li + 2] + 4 * yvar[li + 1] + yvar[li]) / 6
        return quad
        exit()
    elif (n == 3): # Simpson's 3/8 rule
        quad = (xvar[ui] - xvar[li]) * (yvar[li + 3] + 3 * yvar[li + 2] + 3 * yvar[li + 1] + yvar[li]) / 8
        return quad
        exit()
    elif (n % 2):
        ui -= 1
#        raise ValueError('Number of subintervals must be divisble by 2')

    iend = yvar[li] + yvar[ui]; ieven = 0.0; iodd = 0.0; j = li + 1 # endpoints; even terms; odd terms; index
    while (j <= (ui - 1)):
        if not ((j - li) % 2):
            ieven = ieven + 2 * yvar[j]
        else:
            iodd = iodd + 4 * yvar[j]
        j = j + 1

    quad = h / 3 * (iend + ieven + iodd)
    return quad
