import heapq
import Matching


class PairMatching:
    """Class for finding the best user pairings"""

    def __init__(self, users):
        self.__userPairs: __MatchingPair = []
        self.__unmatchedUsers = set()
        self.__CreatePairs(users)
        heapq._heapify_max(self.__userPairs)

    def __CreatePairs(self, users):
        for i in range(len(users)):
            self.__unmatchedUsers.add(users[i])
            for j in range(len(users)):
                self.__userPairs.append(
                    __MatchingPair(
                        users[i], users[j], Matching.Match(users[i], users[j])
                    )
                )

    def findMatch(self):
        """Returns a Tuple containing the user pair and their inner product"""
        while len(self.__userPairs) != 0:
            pair: __MatchingPair = self.__userPairs.pop()
            if (
                pair.user1 in self.__unmatchedUsers
                and pair.user2 in self.__unmatchedUsers
            ):
                self.__unmatchedUsers.remove(pair.user1)
                self.__unmatchedUsers.remove(pair.user2)
                return (pair.user1, pair.user2, pair.data)
        return None


class __MatchingPair:
    """Internal Class used for comparing matching data"""

    def __init__(self, user1, user2, data: float):
        self.user1 = user1
        self.user2 = user2
        self.data = data

    def __lt__(self, other):
        return self.data < other.data

    def __repr__(self):
        return f"({self.user1},{self.user2}) : {self.data}"
