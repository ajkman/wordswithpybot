from gameboard import GameBoard
from tile import Tile

g = GameBoard()

tiles = [
    Tile('C'),
    Tile('A'),
    Tile('T'),
    ]

xpos = [7, 7, 7]
ypos = [7, 8, 9]

for t, i, j in zip(tiles, xpos, ypos):
    g.add_tile_to_move(t, i, j)

result = g.validate_current_move()
if result == GameBoard.INVALID_PLACEMENT:
    print 'Invalid tile placement'
elif result == GameBoard.INVALID_WORD:
    print 'Invalid word:'
    print g.get_invalid_words()
elif result == GameBoard.VALID_MOVE:
    print 'Valid move'

