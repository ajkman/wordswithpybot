class GameSpace(object):
    def __init__(self, global_modifier=1, local_modifier=1):
        self._global_modifier = global_modifier
        self._local_modifier = local_modifier
        self._tile = None

    def set_local_modifier(self, value):
        self._local_modifier = value

    def set_global_modifier(self, value):
        self._global_modifier = value

    def get_local_modifier(self):
        return self._local_modifier

    def get_global_modifier(self):
        return self._global_modifier

    def set_tile(self, tile):
        self._tile = tile

    def occupied(self):
        return self._tile is not None

    def __str__(self):
        if self.occupied():
            return str(self._tile)
        else:
            return "_"
