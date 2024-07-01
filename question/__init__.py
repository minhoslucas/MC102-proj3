from dataclasses import dataclass
import reader

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

questions: dict[str, list[Question]] = \
    {difficulty: [Question(question) for question in qList] 
     for difficulty, qList in reader.questions.items()}
