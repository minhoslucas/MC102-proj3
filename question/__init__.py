from dataclasses import dataclass
import reader
from random import randrange

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

questions: dict[int, list[Question]] = \
    {difficulty: [Question(question) for question in qList] 
     for difficulty, qList in reader.questions.items()}

def select_question(difficulty: int) -> Question:
    pool = questions[difficulty]
    index = randrange(0, len(pool))
    
    return pool.pop(index)

if __name__ == "__main__":
    question = select_question(3)

    assert question not in questions[3]

    assert isinstance(question, Question)

    assert question.difficulty == 3

    assert question.answer in question.choices
