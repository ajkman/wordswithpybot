import config
import gamespace
import wordlist

class GameBoard(object):
    VALID_MOVE = 1
    INVALID_PLACEMENT = 2
    INVALID_WORD = 3

    def __init__(self):
        self._current_move = {}
        self._board = []
        self._wordlist = wordlist.WordList()
        self._invalid_words = []
        self._playable_spaces = [
            (config.number_of_rows / 2 - 1, config.number_of_columns / 2 - 1)
            ]

        for i in range(config.number_of_rows):
            row = []
            for j in range(config.number_of_columns):
                space = gamespace.GameSpace()
                row.append(space)
            
            self._board.append(row)

    def get_invalid_words(self):
        return self._invalid_words

    def add_tile_to_move(self, tile, i, j):
        if not self._board[i][j].occupied():
            self._current_move[(i,j)] = tile

    def validate_current_move(self):
        # First check for valid tile placement
        y_indices, x_indices = zip(*(self._current_move.keys()))
        rowwise = (len(set(y_indices)) == 1)
        columnwise = (len(set(x_indices)) == 1)
        if not rowwise and not columnwise:
            return self.INVALID_PLACEMENT
        elif len(set(zip(y_indices,x_indices)).intersection(self._playable_spaces)) == 0:
            return self.INVALID_PLACEMENT        

        #Build horizontal words
        hwords = []
        for i in range(config.number_of_rows):
            word = ""
            new_word = False
            for j in range(config.number_of_columns):
                gamespace = self._board[i][j]
                if (i, j) in self._current_move:
                    word += self._current_move[(i,j)].get_letter()
                    new_word = True
                elif not gamespace.occupied() and word != "":
                    if new_word:
                        hwords.append(word.lower())

                    word = ""
                    new_word = False
                elif gamespace.occupied():
                    word += gamespace.get_tile().get_letter()

        #Build vertical words
        vwords = []
        for j in range(config.number_of_columns):
            word = ""
            new_word = False
            for i in range(config.number_of_rows):
                gamespace = self._board[i][j]
                if (i, j) in self._current_move:
                    word += self._current_move[(i,j)].get_letter()
                    new_word = True
                elif not gamespace.occupied() and word != "":
                    if new_word:
                        vwords.append(word)

                    word = ""
                    new_word = False
                elif gamespace.occupied():
                    word += gamespace.get_tile().get_letter()

        #Check words
        print "hwords: ", hwords
        print "vwords: ", vwords
        if (rowwise and len(hwords) > 1) or (columnwise and len(vwords) > 1):
            return self.INVALID_PLACEMENT
        
        words = hwords + vwords
        self._invalid_words = [
            w for w in words if not self._wordlist.check_word(w)
            ]
        if len(self._invalid_words) > 0:
            return self.INVALID_WORD

        return self.VALID_MOVE

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



    
