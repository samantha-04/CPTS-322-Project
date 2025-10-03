from math import sqrt, pow

# Finds dot prod. between 2 vectors
# O(n)
def FindDotProduct (p1 : list[int], p2 : list[int]) -> float:
    """
    Calculates the dot product between two given vectors.
    Requires two lists as input.
    """

    if (len(p1) == len(p2)):
        sum = 0

        for i, j in zip(p1, p2):
            sum += i*j

        return sum
    else:
       return 2.0


# Finds unit vector
# O(n)
def FindUnitVector (v : list) -> list[float]:
    """
    Calculates the unit vector for a given vector.
    Requires a list as input.
    """

    res = []
    magnitude = 0

    # Finding vector magnitude.
    for i in v:
        magnitude += pow(i,2)
    magnitude = sqrt(magnitude)

    # Normalizing the vector.
    for i in v:
        res.append(i/magnitude)

    return res

# Determines if a matching is stable.
# O(1)
def Stable (dotProd : float) -> bool:
    """
    Determines if two roommates would be a stable match.
    Requires a float as input.
    """

    if (dotProd > .7):
        return True
    
    return False