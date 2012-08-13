from config import points_map

class Tile(object):
    def __init__(self, letter='BLANK'):
        self._letter = letter.upper()
        self._points = points_map[self._letter]

    def get_letter(self):
        return self._letter

    def get_points(self):
        return self._points

    def set_letter(self, letter):
        self._letter = letter

    def __str__(self):
        return self._letter

    def __repr__(self):
        return "<tile.Tile object: '{0}'>".format(self.get_letter())

