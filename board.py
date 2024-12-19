from tile import Tile

class Board:
    def __init__(self, layout_config=None):
        self.tiles = self.setup_tiles(layout_config)
        self.adjacency_info = self.setup_adjacency()

    def setup_tiles(self, layout_config):
        resources = ["wood", "brick", "sheep", "wheat", "ore", "wood", "brick"]
        numbers = [5, 2, 6, 8, 9, 10, 4]
        return [Tile(r, n) for r, n in zip(resources, numbers)]

    def setup_adjacency(self):
        return {
            "I1": [0, 1, 2],
            "I2": [1, 2, 3],
            "I3": [2, 3, 4],
            "I4": [3, 4, 5],
            "I5": [4, 5, 6],
            "I6": [0, 2, 5],
            "I7": [1, 4, 6]
        }

    def get_resources_for_roll(self, roll_number):
        producing_tiles = []
        for i, t in enumerate(self.tiles):
            if t.number == roll_number and t.resource_type != "desert":
                producing_tiles.append((i, t.resource_type))
        return producing_tiles
