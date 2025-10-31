class MatchingPair:
    def __init__(self, user1, user2, data: float):
        self.user1 = user1
        self.user2 = user2
        self.data = data

    def __lt__(self, other):
        return self.data < other.data

    def __repr__(self):
        return f"({self.user1},{self.user2}) : {self.data}"

    def __iter__(self):
        yield self.user1
        yield self.user2
        yield self.data
