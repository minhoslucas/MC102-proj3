from dataclasses import dataclass
from maze import MazeTemplate, mazes

from save.reader import read, write, clear

@dataclass
class SaveData:
    name: str
    maze: MazeTemplate
    player: tuple[int, int]
    professors: list[tuple[int, int]]
    classmates: list[tuple[int, int]]
    items: dict[str, list[tuple[int, int]]]
    score: int
    time: int
    bombs: int
    life: int
    difficulty: int
    level: int

    def save(self):
        write(self.__dict__)

def load() -> SaveData:
    save = SaveData(**read())
    clear()
    return save

def main():
    save = SaveData("meida", mazes[0], (1, 1), [(3, 4), (5, 8)], [(9, 9)], [("life", (8, 8))], 200, 100, 2, 5, 2, 1)
    save.save()

    del save

    save = load()
    save.save()
    return save

if __name__ == "__main__":
    main()
