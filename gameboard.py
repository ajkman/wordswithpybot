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

        nrow = config.number_of_rows
        ncol = config.number_of_columns
        for i in range(nrow):
            row = []
            for j in range(ncol):
                space = gamespace.GameSpace()
                # Set modifiers on gameboard
                loc_list = [
                    (i, j),
                    (i, ncol - 1 - j),
                    (nrow - 1 - i, j),
                    (nrow - 1 - i, ncol - 1 - j)
                    ]
                modifier = [config.modifiers[l] for l in loc_list if l in config.modifiers]
                if len(modifier) > 0:
                    modifier = modifier[0]
                    if modifier == config.TL:
                        space.set_local_modifier(3)
                    elif modifier == config.TW:
                        space.set_global_modifier(3)
                    elif modifier == config.DL:
                        space.set_local_modifier(2)
                    elif modifier == config.DW:
                        space.set_global_modifier(2)

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

    def finalize_move(self):
        for (i, j), tile in self._current_move.iteritems():
            self._board[i][j].set_tile(tile)

        self._current_move = []

    def get_score(self):
        return self._score

    def find_playable_spaces(self):
        self._playable_spaces = set()
        for i in range(config.number_of_rows):
            for j in range(config.number_of_columns):
                if self._board[i][j].occupied():
                    continue
                if ((i > 0 and self._board[i - 1][j].occupied()) or
                    (j > 0 and self._board[i][j - 1].occupied()) or
                    (i < config.number_of_rows - 1 and self._board[i + 1][j].occupied()) or
                    (j < config.number_of_rows - 1 and self._board[i][j + 1].occupied())):
                    self._playable_spaces.add((i,j))

    def find_move(self, tilelist):
        self.find_playable_spaces()
        letters = set(tile.get_letter() for tile in tilelist)
        letter_class = "[" + "".join(letters) + "]"
        for space in self._playable_spaces:
            horizontal, vertical = self.get_surrounding_letters(space)
            reg = horizontal[0] + letter_class + horizontal[1]
            print reg
            words = self._wordlist.regex_search(reg.lower())
            reg = vertical[0] + letter_class + vertical[1]
            print reg
            words.extend(self._wordlist.regex_search(reg.lower()))

        print len(words)

    def get_surrounding_letters(self, space):
        row, column = space
        # Build up horizontal word (minus the current space)
        preword = ""
        index = column - 1
        while index >= 0 and self._board[row][index].occupied():
            preword = self._board[row][index].get_tile().get_letter() + preword
            index -= 1

        postword = ""
        index = column + 1
        while index < config.number_of_columns and self._board[row][index].occupied():
            postword += self._board[row][index].get_tile().get_letter()
            index += 1

        horizontal = (preword, postword)

        preword = ""
        index = row - 1
        while index >= 0 and self._board[index][column].occupied():
            preword = self._board[index][column].get_tile().get_letter() + preword
            index -= 1

        postword = ""
        index = row + 1
        while index < config.number_of_rows and self._board[index][column].occupied():
            postword += self._board[index][column].get_tile().get_letter()
            index += 1

        vertical = (preword, postword)
        return (horizontal, vertical)


    def get_playable_spaces(self):
        self.find_playable_spaces();
        return self._playable_spaces;

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




