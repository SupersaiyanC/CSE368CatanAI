from q_learning import QLearning
import random
class AIAgent:
    def __init__(self, player, action_space=["build_settlement","build_city","build_road","trade","end_turn"]):
        self.player = player
        self.actions = action_space
        
        self.q_learner = QLearning(
            learning_rate=0.1, 
            discount_factor=0.9, 
            exploration_rate=0.1
        )
        
        self.last_state = None
        self.last_action = None
        
        self.episode_reward = 0.0
        self.rewards_history = []  # store total reward per episode

    def start_new_episode(self):
        """Call this at the start of each episode."""
        self.episode_reward = 0.0
        self.last_state = None
        self.last_action = None

    def end_episode(self, episode_number, total_episodes):
        """Call this at the end of each episode to log progress."""
        self.rewards_history.append(self.episode_reward)
        
        # Compute some statistics
        avg_reward_last_10 = sum(self.rewards_history[-10:]) / min(len(self.rewards_history), 10)
        
        print(f"==== End of Episode {episode_number} ====")
        print(f"Total Reward this episode: {self.episode_reward:.2f}")
        print(f"Average Reward (last 10 eps): {avg_reward_last_10:.2f}")
        print(f"Current Epsilon: {self.q_learner.epsilon:.2f}")
        print(f"Final VP of Player {self.player.id}: {self.player.victory_points}")
        print("==========================================")

        # Performance metric comparing early vs later episodes
        # Only do this if we have at least 20 episodes recorded as a demonstration
        if len(self.rewards_history) >= 20:
            half = len(self.rewards_history) // 2
            early_avg = sum(self.rewards_history[:half]) / half
            late_avg = sum(self.rewards_history[half:]) / (len(self.rewards_history) - half)
            print(f"Early vs Later performance for Player {self.player.id}:")
            print(f" - Early episodes avg reward: {early_avg:.2f}")
            print(f" - Later episodes avg reward: {late_avg:.2f}")
            print("==========================================")

    def get_state(self):
        r = self.player.resources
        return (r["wood"], r["brick"], r["sheep"], r["wheat"], r["ore"], self.player.victory_points)

    def choose_action(self):
        state = self.get_state()
        action = self.q_learner.choose_action(state, self.actions)
        self.last_state = state
        self.last_action = action
        return action

    def update_q_values(self, reward):
        if self.last_state is not None and self.last_action is not None:
            current_state = self.get_state()
            next_actions = self.actions
            self.q_learner.update(self.last_state, self.last_action, reward, current_state, next_actions)
        # Add reward to episode total to monitor improvement
        self.episode_reward += reward

    def have_settlement_resources(self):
        r = self.player.resources
        return r["wood"] >= 1 and r["brick"] >= 1 and r["sheep"] >= 1 and r["wheat"] >= 1

    def have_city_resources(self):
        r = self.player.resources
        return r["wheat"] >= 2 and r["ore"] >= 3 and len(self.player.settlements) > 0

    def perform_action(self, game_state):
        action = self.choose_action()

        target_settlement = self.player.settlements[0] if len(self.player.settlements) > 0 else "I1"

        if action == "build_settlement":
            success = self.player.build_settlement("I1")
            if success:
                return ("build_settlement", 1.0)
            return ("build_settlement", -0.1)

        elif action == "build_city":
            if len(self.player.settlements) > 0:
                success = self.player.build_city(target_settlement)
                if success:
                    return ("build_city", 2.0)
            return ("build_city", -0.1)

        elif action == "build_road":
            success = self.player.build_road("path_1")
            if success:
                return ("build_road", 0.7)
            return ("build_road", -0.1)

        elif action == "trade":
            r = self.player.resources
            traded = False

            if not self.have_settlement_resources():
                if r["brick"]<1 and r["sheep"]>=4:
                    r["sheep"]-=4
                    r["brick"]+=1
                    traded=True
                elif r["brick"]<1 and r["wheat"]>=4:
                    r["wheat"]-=4
                    r["brick"]+=1
                    traded=True

                if not traded and r["wood"]<1 and r["sheep"]>=4:
                    r["sheep"]-=4
                    r["wood"]+=1
                    traded=True
                elif not traded and r["wood"]<1 and r["wheat"]>=4:
                    r["wheat"]-=4
                    r["wood"]+=1
                    traded=True

            if not traded and not self.have_city_resources():
                needed_ore = 3 - r["ore"] if r["ore"]<3 else 0
                while needed_ore > 0 and r["sheep"]>=4:
                    r["sheep"]-=4
                    r["ore"]+=1
                    needed_ore-=1
                    traded=True

                needed_wheat = 2 - r["wheat"] if r["wheat"]<2 else 0
                while needed_wheat >0 and r["sheep"]>=4:
                    r["sheep"]-=4
                    r["wheat"]+=1
                    needed_wheat-=1
                    traded=True

            if traded:
                if self.have_city_resources() or self.have_settlement_resources():
                    return ("trade",0.5)
                return ("trade",0.2)

            return ("trade", -0.1)

        elif action == "end_turn":
            return ("end_turn", -0.1)
