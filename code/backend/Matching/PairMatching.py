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


"""
import random

def generate_Arrays(row: int, col: int) -> list[float]:
    lists = []
    for _ in range(row):
        rand_list = [random.uniform(0, 2) for _ in range(col)]
        lists.append(rand_list)
    return lists


matchtests = PairMatching(generate_Arrays(150, 25))
i = 1
while True:
    res = matchtests.findMatch()
    print(str(i) + ": " + str(res) + " " + str(type(res)) + "\n")
    if res == None:
        break
    i += 1
"""
