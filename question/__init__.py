from dataclasses import dataclass
from question import reader
from random import randrange, shuffle, choice

@dataclass
class Question:
    question: str
    choices: list[str]
    answer: str
    difficulty: int

    def __init__(self, dict):
        super().__init__()
        for key, value in dict.items():
            setattr(self, key, value)

    def shuffle(self):
        shuffle(self.choices)

questions: dict[int, list[Question]] = \
    {difficulty: [Question(question) for question in qList] 
     for difficulty, qList in reader.questions.items()}

def select_question(difficulty: int) -> Question:
    # print(difficulty)

    if difficulty not in questions:
        print("NOT FOUND, SEARCHING ANOTHER...")
        difficulty = choice(list(questions.keys()))

    pool = questions[difficulty]
    index = randrange(0, len(pool))
    
    question = pool.pop(index)
    question.shuffle()

    if len(pool) == 0:
        del questions[difficulty]

    return question

if __name__ == "__main__":
    question = select_question(3)

    assert question not in questions[3]

    assert isinstance(question, Question)

    assert question.difficulty == 3

    assert question.answer in question.choices
