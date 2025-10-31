import heapq
import Matching
from MatchingPair import MatchingPair


class PairMatching:
    """Class for finding the best user pairings"""

    def __init__(self, users: list):
        self.__userPairs: list[MatchingPair] = []
        self.__unmatchedUsers: list[list] = list()
        self.__CreatePairs(users)
        heapq._heapify_max(self.__userPairs)

    def __CreatePairs(self, users):
        for i in range(len(users)):
            self.__unmatchedUsers.append(users[i])
            for j in range(i + 1, len(users)):
                self.__userPairs.append(
                    MatchingPair(users[i], users[j], Matching.Match(users[i], users[j]))
                )

    def findMatch(self) -> tuple:
        """Returns a Tuple containing the user pair and their inner product"""

        while True:
            if len(self.__userPairs) == 0:
                break
            pair: MatchingPair = self.__userPairs.pop(0)
            if (
                pair.user1 in self.__unmatchedUsers
                and pair.user2 in self.__unmatchedUsers
            ):
                self.__unmatchedUsers.remove(pair.user1)
                self.__unmatchedUsers.remove(pair.user2)
                return tuple(pair)
            heapq._heapify_max(self.__userPairs)
        if len(self.__unmatchedUsers) == 1:
            temp = self.__unmatchedUsers[0]
            self.__unmatchedUsers.clear()
            return (temp, None, None)
        else:
            return None


tests = [
    [0.12, 0.45, 0.78],
    [0.34, 0.56, 0.12],
    [0.67, 0.23, 0.89],
    [0.91, 0.34, 0.22],
    [0.15, 0.77, 0.63],
    [0.48, 0.52, 0.94],
    [0.39, 0.61, 0.73],
    [0.25, 0.85, 0.49],
    [0.74, 0.36, 0.27],
    [0.58, 0.92, 0.41],
    [0.13, 0.67, 0.58],
    [0.44, 0.29, 0.88],
    [0.19, 0.53, 0.72],
    [0.83, 0.64, 0.35],
    [0.57, 0.48, 0.66],
    [0.28, 0.75, 0.51],
    [0.96, 0.22, 0.84],
    [0.62, 0.31, 0.79],
    [0.73, 0.94, 0.25],
    [0.85, 0.46, 0.68],
    [0.41, 0.57, 0.19],
    [0.32, 0.81, 0.56],
    [0.27, 0.93, 0.44],
    [0.76, 0.38, 0.53],
    [0.54, 0.69, 0.37],
]
matchtests = PairMatching(tests)
i = 1
while True:
    res = matchtests.findMatch()
    print(str(i) + ": " + str(res) + " " + str(type(res)) + "\n")
    if res == None:
        break
    i += 1
