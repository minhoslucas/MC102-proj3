from dataclasses import dataclass
from leaderboard.reader import add, read

@dataclass
class Score:
    player: str
    time: int
    score: int
    maze: int

    def __lt__(self, other):
        return (self.score, self.player) < (other.score, other.player)

    def save(self) -> bool:
        return add(self.__dict__)

def leaderboard() -> list[Score]:
    leaderboard = [Score(**score) for score in read().values()]
    leaderboard.sort(reverse=True)

    return leaderboard

if __name__ == "__main__":
    from reader import clear

    clear()

    mock_score = Score("meida", 300, 600, 2)
    mock_score.save()

    lb = leaderboard()


    assert lb[0] == mock_score

    mock_score = Score("meida", 250, 600, 2)
    mock_score.save()

    lb = leaderboard()

    assert lb[0].score == mock_score.score

    other_score = Score("lucas", 245, 700, 2)
    other_score.save()

    lb = leaderboard()

    print(lb)

    assert lb[0] == other_score
    assert lb[1] == mock_score

    other_score = Score("meida", 300, 500, 3)
    other_score.save()

    lb = leaderboard()

    print(lb)

    assert lb[0] == mock_score

