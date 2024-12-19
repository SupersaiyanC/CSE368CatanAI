import random

class GameState:
    def __init__(self, players, board):
        self.players = players
        self.board = board
        self.current_player_index = 0
        self.turn_phase = "resource_collection"

    def roll_dice(self):
        return random.randint(1,6) + random.randint(1,6)

    def distribute_resources(self, roll_number):
        producing_tiles = self.board.get_resources_for_roll(roll_number)
        for tile_index, resource_type in producing_tiles:
            for intersection, tiles in self.board.adjacency_info.items():
                if tile_index in tiles:
                    for player in self.players:
                        if intersection in player.cities:
                            player.resources[resource_type] += 2
                        elif intersection in player.settlements:
                            player.resources[resource_type] += 1

    def next_player(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def get_current_player(self):
        return self.players[self.current_player_index]
