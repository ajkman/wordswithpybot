import config
import gamespace

class GameBoard(object):
    VALID_MOVE = 1
    INVALID_PLACEMENT = 2
    INVALID_WORD = 3

    def __init__(self):
        self._current_move = {}
        self._board = []
        self._playable_spaces = [
            (config.number_of_rows / 2 - 1, config.number_of_columns / 2 - 1)
            ]

        for i in range(config.number_of_rows):
            row = []
            for j in range(config.number_of_columns):
                space = gamespace.GameSpace()
                row.append(space)
            
            self._board.append(row)

    def add_tile_to_move(self, tile, i, j):
        if not self._board[i][j].occupied():
            self._current_move[(i,j)] = tile

    def validate_current_move(self):
        # First check for valid tile placement
        x_indices, y_indices = zip(*(self._current_move.keys()))
        rowwise = (len(set(y_indices)) == 1)
        columnwise = (len(set(x_indices)) == 1)
        if not rowwise and not columnwise:
            return self.INVALID_PLACEMENT
        elif len(set(zip(x_indices,y_indices)).intersection(self._playable_spaces)) == 0:
            return self.INVALID_PLACEMENT        

        #Build horizontal words
        words = []
        for i in range(number_of_rows):
            word = ""
            for j in range(number_of_columns):
                gamespace = self._board[i][j]
                if not gamespace.occupied() and word != "":
                    words.append(word)
                    word = ""
                elif gamespace.occupied():
                    word += gamespace.get_tile().get_letter()
                elif (i, j) in self._current_move:
                    word += self._current_move[(i,j)].get_letter()

        #Build vertical words
        for j in range(number_of_columns):
            word = ""
            for i in range(number_of_rows):
                gamespace = self._board[i][j]
                if not gamespace.occupied() and word != "":
                    words.append(word)
                    word = ""
                elif gamespace.occupied():
                    word += gamespace.get_tile().get_letter()
                elif (i, j) in self._current_move:
                    word += self._current_move[(i,j)].get_letter()

        #Check words

    def find_playable_spaces(self):
        self._playable_spaces = set()
        for i in range(config.number_of_rows):
            for j in range(config.number_of_columns):
                if self._board[i][j].occupied:
                    continue
                if ((i > 0 and self._board[i - 1][j].occupied) or
                    (j > 0 and self._board[i][j - 1].occupied) or
                    (i < number_of_rows - 1 and self._board[i + 1][j].occupied) or
                    (j < number_of_rows - 1 and self._board[i][j + 1].occupied)):
                    self._playable_spaces.add((i,j))

    def return_tiles(self):
        tiles = [t[0] for t in self._current_move]
        self._current_move = []
        return tiles

    def __str__(self):
        return str(self._board)

    def __repr__(self):
        return str(self._board)



    
