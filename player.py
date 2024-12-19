class Player:
    def __init__(self, player_id):
        self.id = player_id
        self.resources = {"wood": 0, "brick": 0, "sheep": 0, "wheat": 0, "ore": 0}
        self.settlements = []
        self.cities = []
        self.roads = []
        self.victory_points = 0

    def can_build_settlement(self):
        return all(self.resources[r] >= 1 for r in ["wood", "brick", "sheep", "wheat"])

    def build_settlement(self, location):
        if self.can_build_settlement():
            for r in ["wood", "brick", "sheep", "wheat"]:
                self.resources[r] -= 1
            self.settlements.append(location)
            self.victory_points += 1
            return True
        return False

    def can_build_city(self):
        return len(self.settlements) > 0 and self.resources["wheat"] >= 2 and self.resources["ore"] >= 3

    def build_city(self, location):
        if self.can_build_city() and location in self.settlements:
            self.resources["wheat"] -= 2
            self.resources["ore"] -= 3
            self.settlements.remove(location)
            self.cities.append(location)
            self.victory_points += 1
            return True
        return False

    def can_build_road(self):
        return all(self.resources[r] >= 1 for r in ["wood", "brick"])

    def build_road(self, path_id):
        if self.can_build_road():
            self.resources["wood"] -= 1
            self.resources["brick"] -= 1
            self.roads.append(path_id)
            return True
        return False