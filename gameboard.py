import config
import gamespace

class GameBoard(object):
    INVALID_PLACEMENT = 1

    def __init__(self):
        self._current_move = []
        self._board = []
        for i in range(config.number_of_rows):
            row = []
            for j in range(config.number_of_columns):
                space = gamespace.GameSpace()
                row.append(space)
            
            self._board.append(row)

    def add_tile_to_move(self, tile, i, j):
        if not self._board[i][j].occupied():
            self._current_move.append((tile, i, j))

    def validate_current_move(self):
        # First check for valid tile placement
        tiles, x_indices, y_indices = zip(*self._current_move)
        if len(set(x_indices)) > 1 and len(set(y_indices)) > 1:
            return self.INVALID_PLACEMENT

    def return_tiles(self):
        tiles = [t[0] for t in self._current_move]
        self._current_move = []
        return tiles

    def __str__(self):
        return str(self._board)

    def __repr__(self):
        return str(self._board)



    
