import random
from tile import Tile

class Board:
    def __init__(self, layout_config=None):
        self.tiles = self.setup_tiles(layout_config)
        self.adjacency_info = self.setup_adjacency()
        self.paths = self.generate_paths()

    def setup_tiles(self, layout_config):
        # Define a balanced resource setup with numbers
        resources = ["wood", "brick", "sheep", "wheat", "ore", "wood", "brick", "sheep", "wheat", "ore"]
        numbers = [5, 2, 6, 8, 9, 10, 4, 3, 11, 12]
        if layout_config:
            return [Tile(r, n) for r, n in zip(layout_config['resources'], layout_config['numbers'])]
        return [Tile(r, n) for r, n in zip(resources, numbers)]

    def setup_adjacency(self):
        # Dynamically generate adjacency for a hexagonal board
        adjacency = {
            "I1": ["0", "1", "2"],
            "I2": ["1", "2", "3"],
            "I3": ["2", "3", "4"],
            "I4": ["3", "4", "5"],
            "I5": ["4", "5", "6"],
            "I6": ["0", "2", "5"],
            "I7": ["1", "4", "6"],
            "I8": ["0", "3", "6"],  # Extra intersections
            "I9": ["1", "5", "7"],  # Extra intersections
            "I10": ["3", "6", "7"],  # Extra intersections
        }
        return adjacency

    def generate_paths(self):
        # Create paths as tuples of intersections
        paths = {}
        for intersection, neighbors in self.adjacency_info.items():
            for neighbor in neighbors:
                path = tuple(sorted((intersection, neighbor)))
                paths[path] = True
        return paths


    def get_resources_for_roll(self, roll_number):
        # Find tiles that produce resources for the given dice roll
        producing_tiles = []
        for i, t in enumerate(self.tiles):
            if t.number == roll_number and t.resource_type != "desert":
                producing_tiles.append((i, t.resource_type))
        return producing_tiles
