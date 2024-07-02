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

def leaderboard() -> list[list[Score]]:
    raw_leaderboard = read()
    leaderboard = []

    for maze, scores in raw_leaderboard.items():
        if len(leaderboard) < maze:
            leaderboard += [[] for _ in range(maze - len(leaderboard))]

        leaderboard[maze-1] = [Score(**score) for score in scores.values()]
        leaderboard[maze-1].sort()

    return leaderboard

if __name__ == "__main__":
    from reader import clear

    clear()

    mock_score = Score("meida", 300, 600, 2)
    mock_score.save()

    lb = leaderboard()

    assert lb[mock_score.maze-1][0] == mock_score

    mock_score = Score("meida", 300, 650, 2)
    mock_score.save()

    lb = leaderboard()

    assert lb[mock_score.maze-1][0].score == mock_score.score

