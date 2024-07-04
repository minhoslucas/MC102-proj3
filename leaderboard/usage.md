```py
from leaderboard import Score, leaderboard

# retorna todas as pontuações já ordenadas
scores = leaderboard()

maze2_scores = scores[2]

new_score = Score("nome", time=100, score=400, maze=1)
new_score.save()
```
