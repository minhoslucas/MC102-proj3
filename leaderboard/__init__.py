from dataclasses import dataclass
from reader import add, read

@dataclass
class Score:
    player: str
    time: int
    score: int
    maze: int

    def _orderer(self):
        return self.time, self.score, self.player

    def __lt__(self, other):
        return self._orderer() < other._orderer()

    def save(self):
        add(self.__dict__)

def leaderboard() -> list[Score]:
    leaderboard = read()

    leaderboard = [Score(**score) for score in leaderboard]

    leaderboard.sort()

    return leaderboard

if __name__ == "__main__":
    from reader import clear

    clear()

    mock_score = Score("meida", 300, 600, 2)
    mock_score.save()

    leaderboard = leaderboard()

    assert leaderboard[0] == mock_score

    clear()
