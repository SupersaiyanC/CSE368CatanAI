class Tile:
    def __init__(self, resource_type, number):
        self.resource_type = resource_type  # "wood", "brick", "wheat", "sheep", "ore", or "desert"
        self.number = number  # 2-12 (with one tile possibly being desert which doesn't produce)
