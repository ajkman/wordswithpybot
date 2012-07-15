from gameboard import GameBoard
from tile import Tile

g = GameBoard()
print g

word = 'QUANTUM'

tiles = [Tile(x) for x in word]

row = [6 + i for i in range(len(word))]
col = [7 for i in range(len(word))]

for t, i, j in zip(tiles, row, col):
    g.add_tile_to_move(t, i, j)

result = g.validate_current_move()
if result == GameBoard.INVALID_PLACEMENT:
    print 'Invalid tile placement'
elif result == GameBoard.INVALID_WORD:
    print 'Invalid word:'
    print g.get_invalid_words()
elif result == GameBoard.VALID_MOVE:
    print 'Valid move'
    print 'score: ', g.get_score()

