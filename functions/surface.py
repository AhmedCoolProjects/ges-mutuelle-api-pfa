def surfaceFct(x: list, y: list):
    n = len(x)
    s = 0

    for i in range(0, n):
        if i == n - 1:
            s += y[i] * (x[0] - x[i-1])
        elif i == 0:
            s += y[i] * (x[i+1] - x[n-1])
        else:
            s += y[i] * (x[i+1] - x[i-1])

    s *= 1/2
    return(s)
