import math as m
# Dot Product Function
def FindDotProduct (p1 : list, p2 : list):
    if (len(p1) == len(p2)):
        sum = 0
        for i, j in zip(p1, p2):
            sum += i*j
    else:
       return "Vectors not same length"

# Find Unit Vector
def FindUnitVector (v : list):
    res = []
    magnitude = 0

    #
    for i in v:
        magnitude += m.pow(i,2)
    magnitude = m.sqrt(magnitude)

    #
    for i in v:
        res.append(i/magnitude)

    return res

def StableMatch (dotProd : float):
    if (dotProd > .7):
        return True
    return False