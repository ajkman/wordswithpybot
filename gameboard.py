import config
import gamespace

class GameBoard(object):
    def __init__(self):
        self._board = []
        for i in range(config.number_of_rows):
            row = []
            for j in range(config.number_of_columns):
                space = gamespace.GameSpace()
                row.append(space)
            
            self._board.append(row)

    def __str__(self):
        return str(self._board)

    def __repr__(self):
        return str(self._board)



    
