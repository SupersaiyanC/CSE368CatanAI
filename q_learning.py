import pickle
import random
import os

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
        future_q = max([self.get_q_value(next_state, a) for a in next_actions]) if next_actions else 0.0
        new_q = current_q + self.lr * (reward + self.gamma * future_q - current_q)
        self.q_values[(state, action)] = new_q

    def decay_epsilon(self):
        self.epsilon = max(0.01, self.epsilon * 0.99)

    def save(self, filename):
        with open(filename, "wb") as f:
            pickle.dump(self.q_values, f)

    def load(self, filename):
        if os.path.exists(filename):
            with open(filename, "rb") as f:
                self.q_values = pickle.load(f)