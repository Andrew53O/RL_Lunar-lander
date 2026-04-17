import os
import gymnasium as gym
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque
import random
import matplotlib.pyplot as plt

from utils import plot_training_curves, print_stats, save_checkpoint

# Hyperparameters (you should experiment with these options!)
LEARNING_RATE = 5e-4
GAMMA = 0.99  # Discount factor
EPSILON_START = 1.0
EPSILON_END = 0.01
EPSILON_DECAY = 0.995
BATCH_SIZE = 64
BUFFER_SIZE = 10000
TARGET_UPDATE_FREQ = 10  # Update target network every N episodes

NUM_EPISODES = 1000
CHECKPOINT_FREQ = 100
EVAL_EPISODES = 100
HIDDEN_DIM = 128
SUCCESS_REWARD_THRESHOLD = 200.0
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
OUTPUT_DIR = "outputs/part_b_c"
CHECKPOINT_DIR = os.path.join(OUTPUT_DIR, "checkpoints")

# Create environment
env = gym.make('LunarLander-v3')
state_dim = env.observation_space.shape[0]
action_dim = env.action_space.n

print(f"Using device: {DEVICE}")
print(f"State dimension: {state_dim}")
print(f"Action dimension: {action_dim}")

# TODO: Implement the classes of your agent described in Part B


class QNetwork(nn.Module):
    def __init__(self, state_dim: int, action_dim: int, hidden_dim: int = HIDDEN_DIM):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, action_dim),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


class ReplayBuffer:
    def __init__(self, capacity: int):
        self.buffer = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done) -> None:
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size: int):
        batch = random.sample(self.buffer, batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        return (
            np.array(states, dtype=np.float32),
            np.array(actions, dtype=np.int64),
            np.array(rewards, dtype=np.float32),
            np.array(next_states, dtype=np.float32),
            np.array(dones, dtype=np.float32),
        )

    def __len__(self) -> int:
        return len(self.buffer)


class DQNAgent:
    def __init__(self, state_dim: int, action_dim: int):
        self.action_dim = action_dim
        self.gamma = GAMMA
        self.batch_size = BATCH_SIZE

        self.q_network = QNetwork(state_dim, action_dim).to(DEVICE)
        self.target_network = QNetwork(state_dim, action_dim).to(DEVICE)
        self.target_network.load_state_dict(self.q_network.state_dict())
        self.target_network.eval()

        self.replay_buffer = ReplayBuffer(BUFFER_SIZE)
        self.optimizer = optim.Adam(self.q_network.parameters(), lr=LEARNING_RATE)
        self.loss_fn = nn.SmoothL1Loss()

    def select_action(self, state: np.ndarray, epsilon: float) -> int:
        if random.random() < epsilon:
            return random.randrange(self.action_dim)
        return self.greedy_action(state)

    def greedy_action(self, state: np.ndarray) -> int:
        state_tensor = torch.tensor(state, dtype=torch.float32, device=DEVICE).unsqueeze(0)
        with torch.no_grad():
            q_values = self.q_network(state_tensor)
        return int(torch.argmax(q_values, dim=1).item())

    def store_transition(self, state, action, reward, next_state, done) -> None:
        self.replay_buffer.push(state, action, reward, next_state, done)

    def train_step(self):
        if len(self.replay_buffer) < self.batch_size:
            return None, None

        states, actions, rewards, next_states, dones = self.replay_buffer.sample(self.batch_size)

        states = torch.tensor(states, dtype=torch.float32, device=DEVICE)
        actions = torch.tensor(actions, dtype=torch.long, device=DEVICE)
        rewards = torch.tensor(rewards, dtype=torch.float32, device=DEVICE)
        next_states = torch.tensor(next_states, dtype=torch.float32, device=DEVICE)
        dones = torch.tensor(dones, dtype=torch.float32, device=DEVICE)

        current_q_values = self.q_network(states).gather(1, actions.unsqueeze(1)).squeeze(1)

        with torch.no_grad():
            next_q_values = self.target_network(next_states).max(dim=1).values
            target_q_values = rewards + self.gamma * next_q_values * (1.0 - dones)

        loss = self.loss_fn(current_q_values, target_q_values)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        with torch.no_grad():
            mean_max_q = self.q_network(states).max(dim=1).values.mean().item()

        return loss.item(), mean_max_q

    def update_target_network(self) -> None:
        self.target_network.load_state_dict(self.q_network.state_dict())


os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(CHECKPOINT_DIR, exist_ok=True)

agent = DQNAgent(state_dim, action_dim)

# Training loop
num_episodes = NUM_EPISODES
rewards_history = []
epsilon = EPSILON_START
avg_losses = []
epsilons = []
mean_q_values = []
solved_at = None

for episode in range(num_episodes):
    state, _ = env.reset()  # start a episode
    episode_reward = 0.0
    done = False
    episode_losses = []
    episode_qs = []

    while not done:
        # TODO: select an action
        # (An policy )
        action = agent.select_action(state, epsilon)

        next_state, reward, terminated, truncated, _ = env.step(action)
        done = terminated or truncated

        agent.store_transition(state, action, reward, next_state, done)

        loss, mean_max_q = agent.train_step()
        if loss is not None:
            episode_losses.append(loss)
            episode_qs.append(mean_max_q)

        episode_reward += reward
        state = next_state

    if (episode + 1) % TARGET_UPDATE_FREQ == 0:
        agent.update_target_network()

    epsilon = max(EPSILON_END, epsilon * EPSILON_DECAY)

    rewards_history.append(float(episode_reward))
    avg_losses.append(float(np.mean(episode_losses)) if episode_losses else float("nan"))
    epsilons.append(epsilon)
    mean_q_values.append(float(np.mean(episode_qs)) if episode_qs else float("nan"))

    if solved_at is None and len(rewards_history) >= 100:
        if float(np.mean(rewards_history[-100:])) > SUCCESS_REWARD_THRESHOLD:
            solved_at = episode + 1
            print(f"Environment solved at episode {solved_at}.")

    # TODO: Decay epsilon
    # TODO: Track and log statistics

    if (episode + 1) % CHECKPOINT_FREQ == 0:
        checkpoint_path = os.path.join(CHECKPOINT_DIR, f"dqn_episode_{episode + 1}.pt")
        save_checkpoint(agent, episode + 1, rewards_history, checkpoint_path)

    if episode % 50 == 0:
        avg_loss = avg_losses[-1]
        mean_q = mean_q_values[-1]
        print(
            f"Episode {episode + 1}, Reward: {episode_reward:.2f}, "
            f"Epsilon: {epsilon:.3f}, Loss: {avg_loss:.4f}, Mean Max Q: {mean_q:.4f}"
        )

# Testing
# TODO: Test your trained agent
final_checkpoint = os.path.join(CHECKPOINT_DIR, "dqn_final.pt")
save_checkpoint(agent, num_episodes, rewards_history, final_checkpoint)

metrics = {
    "episode_rewards": rewards_history,
    "avg_losses": avg_losses,
    "epsilons": epsilons,
    "mean_q_values": mean_q_values,
    "solved_at": solved_at,
}
plot_training_curves(metrics, out_dir=OUTPUT_DIR)

test_rewards = []
test_lengths = []
test_successes = 0

for _ in range(EVAL_EPISODES):
    state, _ = env.reset()
    done = False
    episode_reward = 0.0
    episode_length = 0

    while not done:
        action = agent.greedy_action(state)
        next_state, reward, terminated, truncated, _ = env.step(action)
        done = terminated or truncated

        episode_reward += reward
        episode_length += 1
        state = next_state

    test_rewards.append(episode_reward)
    test_lengths.append(episode_length)
    if episode_reward >= SUCCESS_REWARD_THRESHOLD:
        test_successes += 1

eval_stats = {
    "mean_reward": float(np.mean(test_rewards)),
    "std_reward": float(np.std(test_rewards)),
    "min_reward": float(np.min(test_rewards)),
    "max_reward": float(np.max(test_rewards)),
    "mean_length": float(np.mean(test_lengths)),
    "success_rate": test_successes / EVAL_EPISODES,
}

print()
print("Evaluation over 100 no-exploration episodes")
print_stats(eval_stats)
print(f"Final checkpoint saved to: {final_checkpoint}")

env.close()
