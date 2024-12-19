class Player:
    def __init__(self, player_id):
        self.id = player_id
        self.resources = {
            "wood": 0,
            "brick": 0,
            "sheep": 0,
            "wheat": 0,
            "ore": 0
        }
        self.settlements = []
        self.cities = []
        self.roads = []
        self.victory_points = 0

    def can_build_settlement(self):
        can = (self.resources["wood"] >= 1 and 
               self.resources["brick"] >= 1 and 
               self.resources["sheep"] >= 1 and 
               self.resources["wheat"] >= 1)
        return can

    def build_settlement(self, location):
        # Check again
        if self.can_build_settlement():
            # Deduct resources
            self.resources["wood"] -= 1
            self.resources["brick"] -= 1
            self.resources["sheep"] -= 1
            self.resources["wheat"] -= 1
            self.settlements.append(location)
            self.victory_points += 1
            return True
        return False

    def can_build_city(self):
        # Need a settlement to upgrade
        if len(self.settlements) == 0:
            return False
        can = (self.resources["wheat"] >= 2 and self.resources["ore"] >= 3)

        return can

    def build_city(self, location):
        if self.can_build_city() and location in self.settlements:
            self.resources["wheat"] -= 2
            self.resources["ore"] -= 3
            self.settlements.remove(location)
            self.cities.append(location)
            self.victory_points += 2  # city is worth 2 VPs total (1 more than a settlement)
            return True
        return False

    def can_build_road(self):
        # road costs: 1 wood, 1 brick
        can = (self.resources["wood"] >= 1 and self.resources["brick"] >= 1)

        return can

    def build_road(self, path_id):
        if self.can_build_road():
            self.resources["wood"] -= 1
            self.resources["brick"] -= 1
            self.roads.append(path_id)
            return True
        return False
