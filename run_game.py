from board import Board
from player import Player
from game_state import GameState
from ai_agent import AIAgent
import random
import matplotlib.pyplot as plt
import numpy as np

def main():
    EPISODES = 10000
    MAX_TURNS = 1000

    total_wins = [0] * 4  # Track wins per player
    total_rewards = [0.0] * 4  # Track total rewards per player
    total_settlements = [0] * 4
    total_cities = [0] * 4

    # For tracking performance over time
    average_rewards_per_episode = [[] for _ in range(4)]
    total_victories = [0] * EPISODES
    average_victory_points = [[] for _ in range(4)]

    for episode in range(EPISODES):
        board = Board()
        players = [Player(i) for i in range(4)]
        game_state = GameState(players, board)

        # List of starting intersections
        starting_intersections = ["I1", "I2", "I3", "I4"]
        
        # Shuffle the starting intersections
        random.shuffle(starting_intersections)

        # Assign shuffled starting settlements to players
        for i, p in enumerate(players):
            p.settlements.append(starting_intersections[i])
            p.victory_points += 1

        agents = [AIAgent(p) for p in players]

        # Start new episode for each agent
        for agent in agents:
            agent.q_learner.decay_epsilon(current_episode=episode + 1, total_episodes=EPISODES)

        turn_count = 0
        episode_ended = False

        while turn_count < MAX_TURNS:
            turn_count += 1
            current_player = game_state.get_current_player()
            agent_index = game_state.current_player_index
            agent = agents[agent_index]

            roll = game_state.roll_dice()
            game_state.distribute_resources(roll)

            action, immediate_reward = agent.perform_action(game_state)

            # Intermediate rewards for resource combinations
            if agent.have_settlement_resources():
                immediate_reward += 0.2
            if agent.have_city_resources():
                immediate_reward += 0.5

            # Reward proportional to VP
            immediate_reward += (current_player.victory_points * 0.01)

            # Check win condition
            if current_player.victory_points >= 10:
                agent.update_q_values(immediate_reward + 10)
                print(f"Player {current_player.id} wins with {current_player.victory_points} VP in episode {episode+1}!")
                total_wins[current_player.id] += 1
                total_victories[episode] += 1
                episode_ended = True
                break
            else:
                agent.update_q_values(immediate_reward)

            game_state.next_player()

        if not episode_ended:
            print("Episode ended due to turn limit.")
            # Final VP-based reward
            for i, p in enumerate(players):
                agents[i].update_q_values(p.victory_points * 0.1)

        # End the episode for each agent - print out improvements
        for i, a in enumerate(agents):
            a.end_episode(episode_number=episode+1, total_episodes=EPISODES)
            total_rewards[i] += a.episode_reward
            average_rewards_per_episode[i].append(a.episode_reward)
            average_victory_points[i].append(players[i].victory_points)

        # Track total settlements and cities
        for i, p in enumerate(players):
            total_settlements[i] += len(p.settlements)
            total_cities[i] += len(p.cities)

        # Decay epsilon dynamically based on performance trends
        for a in agents:
            a.q_learner.decay_epsilon()

        print(f"After Episode {episode+1}, new Epsilon: {agents[0].q_learner.epsilon:.2f}")

        print(f"\nFinal State of Episode {episode+1}")
        for p in players:
            print(f"Player {p.id} VP: {p.victory_points}, Resources: {p.resources}")

    # Print cumulative statistics
    print("\n==========================")
    print("Cumulative Statistics")
    print("==========================")
    for i in range(4):
        avg_reward = total_rewards[i] / EPISODES
        print(f"Player {i}:")
        print(f"  Wins: {total_wins[i]}")
        print(f"  Average Reward: {avg_reward:.2f}")
        print(f"  Total Settlements Built: {total_settlements[i]}")
        print(f"  Total Cities Built: {total_cities[i]}")

    # Plot trends
    episodes = np.arange(EPISODES)
    for i in range(4):
        plt.figure()
        plt.plot(episodes, average_rewards_per_episode[i], label=f"Player {i} Average Rewards")
        plt.xlabel("Episode")
        plt.ylabel("Average Reward")
        plt.title(f"Player {i} Reward Trends")
        plt.legend()
        plt.show()

    plt.figure()
    plt.plot(episodes, total_victories, label="Total Victories per Episode")
    plt.xlabel("Episode")
    plt.ylabel("Victories")
    plt.title("Total Victories per Episode")
    plt.legend()
    plt.show()

    # Compare early vs late episodes
    early_avg_vp = [np.mean(average_victory_points[i][:1000]) for i in range(4)]
    late_avg_vp = [np.mean(average_victory_points[i][-1000:]) for i in range(4)]

    print("\nComparison of Early vs Late Episodes")
    for i in range(4):
        print(f"Player {i}:")
        print(f"  Early Average VP (0-1000): {early_avg_vp[i]:.2f}")
        print(f"  Late Average VP (9000-10000): {late_avg_vp[i]:.2f}")

if __name__ == "__main__":
    main()
