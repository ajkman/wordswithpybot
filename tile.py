from config import points_map

class Tile(object):
    def __init__(self, letter='BLANK'):
        self._letter = letter
        self._points = points_map[self._letter]

    def get_letter(self):
        return self._letter

    def get_points(self):
        return self._points

    def set_letter(self, letter):
        self._letter = letter