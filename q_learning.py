import random

class QLearning:
    def __init__(self, learning_rate=0.1, discount_factor=0.9, exploration_rate=0.1):
        self.q_values = {}
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = exploration_rate

    def get_q_value(self, state, action):
        return self.q_values.get((state, action), 0.0)

    def choose_action(self, state, possible_actions):
        if random.random() < self.epsilon:
            return random.choice(possible_actions)
        else:
            q_values = [self.get_q_value(state, a) for a in possible_actions]
            max_q = max(q_values)
            best_actions = [a for a, q in zip(possible_actions, q_values) if q == max_q]
            return random.choice(best_actions)

    def update(self, state, action, reward, next_state, next_actions):
        current_q = self.get_q_value(state, action)
        future_q = 0.0
        if next_actions:
            future_q = max([self.get_q_value(next_state, a) for a in next_actions])
        new_q = current_q + self.lr * (reward + self.gamma * future_q - current_q)
        self.q_values[(state, action)] = new_q

    def decay_epsilon(self, current_episode=None, total_episodes=None, performance_metric=None, threshold=5):
        """
        Decay epsilon dynamically based on the episode progress or performance metric.

        Args:
            current_episode (int): The current episode number.
            total_episodes (int): The total number of episodes.
            performance_metric (float): A performance metric to adjust epsilon decay.
            threshold (float): The threshold for performance-based decay.
        """
        if current_episode is not None and total_episodes is not None:
            # Linearly decay epsilon based on training progress
            progress = current_episode / total_episodes
            self.epsilon = max(0.01, 0.1 * (1 - progress))  # Example: Scale down from 0.1 to 0.01 linearly
        else:
            # Default decay (use if no episodes provided)
            self.epsilon = max(0.01, self.epsilon * 0.99)

        if performance_metric is not None:
            # Adjust decay based on performance
            if performance_metric > threshold:  # If performance exceeds the threshold, decay faster
                self.epsilon = max(0.01, self.epsilon * 0.95)  # Faster decay for high performance

# Example usage:
# q_learning = QLearning()
# q_learning.decay_epsilon(current_episode=50, total_episodes=100, performance_metric=6, threshold=5)
