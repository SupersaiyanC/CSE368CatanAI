import random
import csv
import time  # Added for profiling
from board import Board
from player import Player
from game_state import GameState
from ai_agent import AIAgent

print("Running Catan Game Simulation")

def random_start_positions(board, players):
    valid_intersections = list(board.adjacency_info.keys())
    used_intersections = set()
    max_attempts = 100  # Keep this to prevent infinite loops

    for player in players:
        attempts = 0
        while attempts < max_attempts:
            s1, s2 = random.sample(valid_intersections, 2)
            if s1 not in used_intersections and s2 not in used_intersections:
                used_intersections.update([s1, s2])
                player.settlements.extend([s1, s2])

                # Assign a road between these two settlements if valid
                road = tuple(sorted((s1, s2)))
                if road in board.paths:
                    player.roads.append(road)
                print(f"Player {player.id} settlements: {s1}, {s2}, road: {road}")
                break
            attempts += 1

        if attempts == max_attempts:
            print(f"Failed intersections: {valid_intersections}")
            raise ValueError(f"Failed to assign starting positions for Player {player.id} after {max_attempts} attempts.")


def main():
    EPISODES = 100
    MAX_TURNS = 200
    SAVE_FILE = "q_values.pkl"
    BASELINE_FILE = "performance.csv"

    # Track performance metrics
    episode_rewards_player = [[] for _ in range(4)]  # track rewards for each player per episode
    episode_wins = [0 for _ in range(4)]  # count wins per player

    print("Starting main loop...")

    for episode in range(EPISODES):
        print(f"Starting Episode {episode + 1}...")
        start_time = time.time()

        # Initialize board and players
        print("Checkpoint: Initializing board...")
        board = Board()

        print("Checkpoint: Initializing players...")
        players = [Player(i) for i in range(4)]

        print("Checkpoint: Initializing game state...")
        game_state = GameState(players, board)

        print("Checkpoint: Assigning random start positions...")
        random_start_positions(board, players)

        print("Checkpoint: Initializing agents...")
        agents = [AIAgent(p) for p in players]

        for agent in agents:
            agent.load_q_values(SAVE_FILE)

        for agent in agents:
            agent.start_new_episode()

        turn_count = 0
        episode_ended = False
        winner_id = None

        while turn_count < MAX_TURNS:
            turn_count += 1

            print(f"Turn {turn_count} of Episode {episode + 1}...")
            current_player = game_state.get_current_player()
            agent_index = game_state.current_player_index
            agent = agents[agent_index]

            print("Rolling dice...")
            roll = game_state.roll_dice()
            print(f"Rolled: {roll}")

            print("Distributing resources...")
            game_state.distribute_resources(roll)
            print("Resources distributed.")

            print("Performing action...")
            action, immediate_reward = agent.perform_action(game_state)
            print(f"Action performed: {action}, Reward: {immediate_reward}")

            if agent.have_settlement_resources():
                immediate_reward += 0.2
            if agent.have_city_resources():
                immediate_reward += 0.5

            immediate_reward += (current_player.victory_points * 0.01)

            if current_player.victory_points >= 10:
                agent.update_q_values(immediate_reward + 10)
                winner_id = current_player.id
                print(f"Player {current_player.id} wins with {current_player.victory_points} VP in episode {episode + 1}!")
                episode_ended = True
                break
            else:
                agent.update_q_values(immediate_reward)

            game_state.next_player()

        if not episode_ended:
            print("Episode ended due to turn limit.")
            for i, p in enumerate(players):
                agents[i].update_q_values(p.victory_points * 0.1)

        for i, a in enumerate(agents):
            a.end_episode()
            episode_rewards_player[i].append(a.episode_reward)

        if winner_id is not None:
            episode_wins[winner_id] += 1

        for a in agents:
            a.q_learner.decay_epsilon()

        if (episode + 1) % 10 == 0:
            agents[0].save_q_values(SAVE_FILE)

        print(f"\nFinal State of Episode {episode + 1}")
        for p in players:
            print(f"Player {p.id} VP: {p.victory_points}, Resources: {p.resources}")

        if (episode + 1) % 10 == 0:
            avg_rewards = [sum(r[-10:]) / 10 for r in episode_rewards_player]
            win_rate = [w / (episode + 1) for w in episode_wins]
            print("Performance after episode", episode + 1)
            for i in range(4):
                print(f"Player {i} - Avg Reward (last 10 eps): {avg_rewards[i]:.2f}, Win Rate: {win_rate[i] * 100:.2f}%")

            with open(BASELINE_FILE, "a", newline="") as f:
                writer = csv.writer(f)
                for i in range(4):
                    writer.writerow([episode + 1, i, avg_rewards[i], win_rate[i]])

        print(f"Episode {episode + 1} completed in {time.time() - start_time:.2f}s")

    print("Final Performance after all episodes:")
    total_episodes = EPISODES
    for i in range(4):
        overall_avg = sum(episode_rewards_player[i]) / total_episodes
        overall_win_rate = (episode_wins[i] / total_episodes) * 100
        print(f"Player {i} - Overall Avg Reward: {overall_avg:.2f}, Overall Win%: {overall_win_rate:.2f}%")

if __name__ == "__main__":
    main()
