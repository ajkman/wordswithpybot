import random
import config
from tile import Tile

class TileStore(object):
    def __init__(self):
        self._tiles = []
        for key, value in config.multiplicity.iteritems():
            self._tiles.extend([Tile(key) for i in range(value)])

        random.shuffle(self._tiles)

    def get_tiles(self):
        return self._tiles

    def get_n_tiles(self, n):
        retval = self._tiles[:n]
        self._tiles = self._tiles[n:]
        return retval


