import heapq
import Matching


class PairMatching:
    """Class for finding best user pairings"""

    def __init__(self, users):
        self.__userPairs: __MatchingPair = []
        self.__matchedUsers = []
        self.__CreatePairs(users)
        heapq._heapify_max(self.__userPairs)

    def __CreatePairs(self, users):
        for i in range(len(users)):
            for j in range(len(users)):
                self.__userPairs.append(
                    __MatchingPair(
                        users[i], users[j], Matching.Match(users[i], users[j])
                    )
                )

    def findMatch(self):
        while len(self.__userPairs) != 0:
            pair: __MatchingPair = self.__userPairs.pop()
            if pair.user1 in self.__matchedUsers or pair.user2 in self.__matchedUsers:
                continue
            else:
                self.__matchedUsers.append(pair.user1)
                self.__matchedUsers.append(pair.user2)
                return (pair.user1, pair.user2, pair.data)


class __MatchingPair:

    def __init__(self, user1, user2, data: float):
        self.user1 = user1
        self.user2 = user2
        self.data = data

    def __lt__(self, other):
        return self.data < other.data

    def __repr__(self):
        return f"({self.user1},{self.user2}) : {self.data}"
