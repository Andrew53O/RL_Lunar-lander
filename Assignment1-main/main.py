import argparse
from datetime import datetime
import fcntl
import os
import gymnasium as gym
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque
import random
import time
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

NUM_EPISODES = 650
CHECKPOINT_FREQ = 50
EVAL_EPISODES = 100
HIDDEN_DIM = 128
SUCCESS_REWARD_THRESHOLD = 200.0
MAX_STEPS_PER_EPISODE = 500
BASE_OUTPUT_DIR = "outputs/part_b"
STATS_PATH = "stats.md"
ALGORITHM_NAME = "Vanilla DQN"

parser = argparse.ArgumentParser(description="Train a Vanilla DQN on LunarLander-v3")
parser.add_argument(
    "--device",
    choices=["auto", "cpu", "cuda"],
    default="auto",
    help="Choose which device to use for PyTorch computations.",
)
parser.add_argument("--run-name", type=str, default=None, help="Optional explicit run folder name.")
parser.add_argument("--learning-rate", type=float, default=LEARNING_RATE, help="Override learning rate.")
parser.add_argument("--epsilon-decay", type=float, default=EPSILON_DECAY, help="Override epsilon decay.")
parser.add_argument(
    "--target-update-freq",
    type=int,
    default=TARGET_UPDATE_FREQ,
    help="Override target network update frequency.",
)
parser.add_argument("--batch-size", type=int, default=BATCH_SIZE, help="Override batch size.")
parser.add_argument("--num-episodes", type=int, default=NUM_EPISODES, help="Override number of episodes.")
parser.add_argument(
    "--max-steps-per-episode",
    type=int,
    default=MAX_STEPS_PER_EPISODE,
    help="Override manual per-episode step cap.",
)
args = parser.parse_args()

if args.device == "cpu":
    DEVICE = torch.device("cpu")
elif args.device == "cuda":
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA was requested, but no CUDA device is available.")
    DEVICE = torch.device("cuda")
else:
    DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

LEARNING_RATE = args.learning_rate
EPSILON_DECAY = args.epsilon_decay
TARGET_UPDATE_FREQ = args.target_update_freq
BATCH_SIZE = args.batch_size
NUM_EPISODES = args.num_episodes
MAX_STEPS_PER_EPISODE = args.max_steps_per_episode

# Create environment
env = gym.make('LunarLander-v3')
state_dim = env.observation_space.shape[0]
action_dim = env.action_space.n

print(f"Requested device mode: {args.device}")
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


def format_duration(seconds: float) -> str:
    total_seconds = int(round(seconds))
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def append_run_stats(
    stats_path: str,
    run_name: str,
    algorithm_name: str,
    num_episodes: int,
    eval_episodes: int,
    requested_device: str,
    actual_device: str,
    elapsed_seconds: float,
    solved_at,
    eval_mean_reward: float,
    hyperparameters: dict,
) -> None:
    solved_value = solved_at if solved_at is not None else "Not solved"
    duration_text = format_duration(elapsed_seconds)
    run_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = (
        "# Run Stats\n\n"
        "Each completed `main.py` training run appends one row here.\n\n"
        "| Run Time | Run | Algorithm | Train Episodes | Eval Episodes | "
        "Requested Device | Actual Device | Duration | Solved At | Eval Mean Reward | "
        "LR | Epsilon Decay | Target Update |\n"
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
    )
    row = (
        f"| {run_time} | {run_name} | {algorithm_name} | {num_episodes} | {eval_episodes} | "
        f"{requested_device} | {actual_device} | {duration_text} | "
        f"{solved_value} | {eval_mean_reward:.2f} | "
        f"{hyperparameters['learning_rate']} | {hyperparameters['epsilon_decay']} | "
        f"{hyperparameters['target_update_freq']} |\n"
    )

    with open(stats_path, "a+", encoding="utf-8") as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        f.seek(0)
        content = f.read()
        if "| Run Time | Run | Algorithm |" not in content:
            f.seek(0, os.SEEK_END)
            if content and not content.endswith("\n"):
                f.write("\n")
            if content:
                f.write("\n")
            f.write(header)
        f.write(row)
        f.flush()
        os.fsync(f.fileno())
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)


def get_run_dir(base_output_dir: str, requested_run_name: str | None = None) -> str:
    os.makedirs(base_output_dir, exist_ok=True)

    if requested_run_name:
        run_dir = os.path.join(base_output_dir, requested_run_name)
        os.mkdir(run_dir)
        return run_dir

    run_number = 1
    while True:
        run_dir = os.path.join(base_output_dir, f"run{run_number}")
        try:
            os.mkdir(run_dir)
            return run_dir
        except FileExistsError:
            run_number += 1


def write_run_summary(
    run_dir: str,
    run_name: str,
    algorithm_name: str,
    requested_device: str,
    actual_device: str,
    elapsed_seconds: float,
    num_episodes: int,
    eval_episodes: int,
    solved_at,
    hyperparameters: dict,
    eval_stats: dict,
) -> None:
    summary_path = os.path.join(run_dir, "run_summary.md")
    solved_value = solved_at if solved_at is not None else "Not solved"

    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(f"# {run_name} Summary\n\n")
        f.write("## Run Info\n\n")
        f.write(f"- Algorithm: {algorithm_name}\n")
        f.write(f"- Requested device: {requested_device}\n")
        f.write(f"- Actual device: {actual_device}\n")
        f.write(f"- Train episodes: {num_episodes}\n")
        f.write(f"- Evaluation episodes: {eval_episodes}\n")
        f.write(f"- Duration: {format_duration(elapsed_seconds)}\n")
        f.write(f"- Solved at: {solved_value}\n\n")

        f.write("## Hyperparameters\n\n")
        f.write("| Parameter | Value |\n")
        f.write("| --- | --- |\n")
        for key, value in hyperparameters.items():
            f.write(f"| {key} | {value} |\n")

        f.write("\n## Evaluation Stats\n\n")
        f.write("| Metric | Value |\n")
        f.write("| --- | --- |\n")
        f.write(f"| mean_reward | {eval_stats['mean_reward']:.2f} |\n")
        f.write(f"| std_reward | {eval_stats['std_reward']:.2f} |\n")
        f.write(f"| min_reward | {eval_stats['min_reward']:.2f} |\n")
        f.write(f"| max_reward | {eval_stats['max_reward']:.2f} |\n")
        f.write(f"| mean_length | {eval_stats['mean_length']:.1f} |\n")
        f.write(f"| success_rate | {eval_stats['success_rate'] * 100:.1f}% |\n")


OUTPUT_DIR = get_run_dir(BASE_OUTPUT_DIR, args.run_name)
CHECKPOINT_DIR = os.path.join(OUTPUT_DIR, "checkpoints")
RUN_NAME = os.path.basename(OUTPUT_DIR)

os.makedirs(CHECKPOINT_DIR, exist_ok=True)

agent = DQNAgent(state_dim, action_dim)
run_start_time = time.perf_counter()

run_hyperparameters = {
    "learning_rate": LEARNING_RATE,
    "gamma": GAMMA,
    "epsilon_start": EPSILON_START,
    "epsilon_end": EPSILON_END,
    "epsilon_decay": EPSILON_DECAY,
    "batch_size": BATCH_SIZE,
    "buffer_size": BUFFER_SIZE,
    "target_update_freq": TARGET_UPDATE_FREQ,
    "num_episodes": NUM_EPISODES,
    "eval_episodes": EVAL_EPISODES,
    "hidden_dim": HIDDEN_DIM,
    "success_reward_threshold": SUCCESS_REWARD_THRESHOLD,
    "max_steps_per_episode": MAX_STEPS_PER_EPISODE,
}

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
    episode_steps = 0
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
        episode_steps += 1

        # Stop overly long hover/drift episodes so training does not stall on one bad policy.
        if episode_steps >= MAX_STEPS_PER_EPISODE:
            done = True

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

    if episode % 10 == 0: # print every 10 episode
        avg_loss = avg_losses[-1]
        mean_q = mean_q_values[-1]
        print(
            f"Episode {episode + 1}, Reward: {episode_reward:.2f}, "
            f"Epsilon: {epsilon:.3f}, Loss: {avg_loss:.4f}, Mean Max Q: {mean_q:.4f}"
        )

# Testing using trained model for NUM_EPISODES times 
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

        if episode_length >= MAX_STEPS_PER_EPISODE:
            done = True

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
print("Evaluation over 100 no-exploration(learned policy) episodes") # testing the learned policy 
print_stats(eval_stats)
print(f"Final checkpoint saved to: {final_checkpoint}")

elapsed_seconds = time.perf_counter() - run_start_time
append_run_stats(
    stats_path=STATS_PATH,
    run_name=RUN_NAME,
    algorithm_name=ALGORITHM_NAME,
    num_episodes=num_episodes,
    eval_episodes=EVAL_EPISODES,
    requested_device=args.device,
    actual_device=str(DEVICE),
    elapsed_seconds=elapsed_seconds,
    solved_at=solved_at,
    eval_mean_reward=eval_stats["mean_reward"],
    hyperparameters=run_hyperparameters,
)
write_run_summary(
    run_dir=OUTPUT_DIR,
    run_name=RUN_NAME,
    algorithm_name=ALGORITHM_NAME,
    requested_device=args.device,
    actual_device=str(DEVICE),
    elapsed_seconds=elapsed_seconds,
    num_episodes=num_episodes,
    eval_episodes=EVAL_EPISODES,
    solved_at=solved_at,
    hyperparameters=run_hyperparameters,
    eval_stats=eval_stats,
)
print(f"Run stats appended to: {STATS_PATH}")
print(f"Total run time: {format_duration(elapsed_seconds)}")
print(f"Run outputs saved to: {OUTPUT_DIR}")

env.close()
