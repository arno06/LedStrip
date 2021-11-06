
def rgb2hsl(pR, pG, pB):
    r = pR / 255
    g = pG / 255
    b = pB / 255
    minV = min(r, g, b)
    maxV = max(r, g ,b)
    d = maxV - minV
    l = (minV + maxV) / 2

    if d==0:
        h = s = 0
    else:
        s = (d / (maxV + minV)) if (l < .5) else (d / (2 - maxV - minV))
        dr = (((maxV - r) / 6) + (d / 2)) / d
        dg = (((maxV - g) / 6) + (d / 2)) / d
        db = (((maxV - b) / 6) + (d / 2)) / d

        if maxV == r:
            h = db - dg
        elif maxV == g:
            h = (1 / 3) + (dr - db)
        elif maxV == b:
            h = (2 / 3) + dg - dr
    return {'h':h, 's':s, 'l':l}


def hsl2rgb(pH, pS, pL):
    if pS == 0:
        r = pL * 255
        g = pL * 255
        b = pL * 255
    else:
        t2 = (pL * (1 + pS)) if (pL < .5) else ((pL + pS) - (pS * pL))
        t1 = (2 * pL) - t2
        r = 255 * hue2rgb(t1, t2, pH + (1 / 3))
        g = 255 * hue2rgb(t1, t2, pH)
        b = 255 * hue2rgb(t1, t2, pH - (1 / 3))
    return {'r':r, 'g':g, 'b':b}


def hue2rgb(pT1, pT2, pH):
    if pH < 0:
        pH = pH + 1
    elif pH > 1:
        pH = pH - 1
    if (6 * pH) < 1:
        return pT1 + (pT2 - pT1) * 6 * pH
    if (2 * pH) < 1:
        return pT2
    if (3 * pH) < 2:
        return pT1 + (pT2 - pT1) * ((2/3) - pH) * 6
    return pT1