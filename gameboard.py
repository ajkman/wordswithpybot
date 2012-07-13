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
        self._score = 0
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
        if len(self._current_move) == 0:
            return self.INVALID_PLACEMENT

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
            global_modifier = 0
            score = 0
            for j in range(config.number_of_columns):
                gamespace = self._board[i][j]
                if (i, j) in self._current_move:
                    tile = self._current_move[(i, j)]
                    word += tile.get_letter()
                    global_modifier *= gamespace.get_global_modifier()
                    score += gamespace.get_local_modifier() * tile.get_points()
                    new_word = True
                elif not gamespace.occupied() and word != "":
                    if new_word and len(word) > 1:
                        hwords.append((word, score * global_modifier))

                    word = ""
                    global_modifier = 0
                    score = 0
                    new_word = False
                elif gamespace.occupied():
                    tile = gamespace.get_tile()
                    word += tile.get_letter()
                    global_modifier *= gamespace.get_global_modifier()
                    score += tile.get_points() * gamespace.get_local_modifier()

        #Build vertical words
        vwords = []
        for j in range(config.number_of_columns):
            word = ""
            new_word = False
            global_modifier = 1.0
            score = 0
            for i in range(config.number_of_rows):
                gamespace = self._board[i][j]
                if (i, j) in self._current_move:
                    tile = self._current_move[(i, j)]
                    word += tile.get_letter()
                    global_modifier *= gamespace.get_global_modifier()
                    score += gamespace.get_local_modifier() * tile.get_points()
                    new_word = True
                elif not gamespace.occupied() and word != "":
                    if new_word and len(word) > 1:
                        vwords.append((word, score * global_modifier))

                    word = ""
                    global_modifier = 0
                    score = 0
                    new_word = False
                elif gamespace.occupied():
                    tile = gamespace.get_tile()
                    word += tile.get_letter()
                    global_modifier *= gamespace.get_global_modifier()
                    score += tile.get_points() * gamespace.get_local_modifier()

        #Check words
        print "hwords: ", hwords
        print "vwords: ", vwords
        if (rowwise and len(hwords) > 1) or (columnwise and len(vwords) > 1):
            return self.INVALID_PLACEMENT

        words = hwords + vwords
        if len(words) == 0:
            return self.INVALID_WORD

        self._invalid_words = [
            w for w,s in words if not self._wordlist.check_word(w.lower())
            ]
        if len(self._invalid_words) > 0:
            return self.INVALID_WORD

        self._score = sum(s for w,s in words)

        return self.VALID_MOVE

    def get_score(self):
        return self._score

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
        self._invalid_words = []
        self._score = 0
        return tiles

    def __str__(self):
        return str(self._board)

    def __repr__(self):
        return str(self._board)




