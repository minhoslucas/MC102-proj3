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

    def save(self) -> bool:
        return add(self.__dict__)

def leaderboard() -> dict[int, list[Score]]:
    raw_leaderboard = read()
    leaderboard = {}

    for maze, scores in raw_leaderboard.items():
        leaderboard[maze] = [Score(**score) for score in scores.values()]
        leaderboard[maze].sort()

    return leaderboard

if __name__ == "__main__":
    from reader import clear

    clear()

    mock_score = Score("meida", 300, 600, 2)
    mock_score.save()

    lb = leaderboard()

    assert lb[mock_score.maze][0] == mock_score

    mock_score = Score("meida", 250, 600, 2)
    mock_score.save()

    lb = leaderboard()

    assert lb[mock_score.maze][0].score == mock_score.score

    other_score = Score("lucas", 245, 700, 2)
    other_score.save()

    lb = leaderboard()

    assert lb[other_score.maze][0] == other_score
    assert lb[other_score.maze][1] == mock_score

    other_score = Score("meida", 300, 500, 3)
    other_score.save()

    lb = leaderboard()

    assert lb[3][0] == other_score

