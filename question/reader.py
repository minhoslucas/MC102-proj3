from os import path
import yaml

questions = {}

with open(path.join("assets", "questions.yml")) as stream:
    parsed = yaml.safe_load(stream)

    for question in parsed["questions"]:
        if (difficulty := question["difficulty"]) not in questions:
            questions[difficulty] = [question]
        else:
            question[difficulty].append(question)
