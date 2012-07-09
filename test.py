from gameboard import GameBoard
from tile import Tile

g = GameBoard()

tiles = [
    Tile('C'),
    Tile('A'),
    Tile('T'),
    ]

xpos = [0, 1, 2]
ypos = [0, 0, 1]

for t, i, j in zip(tiles, xpos, ypos):
    g.add_tile_to_move(t, i, j)

result = g.validate_current_move()
if result == GameBoard.INVALID_PLACEMENT:
    print 'Invalid tile placement'
