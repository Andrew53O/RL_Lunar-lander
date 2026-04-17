import os

import gymnasium as gym
import numpy as np

from utils import plot_baseline, print_stats, record_episodes


ENV_NAME = "LunarLander-v3"
NUM_EPISODES = 100
NUM_RECORD_EPISODES = 3
OUTPUT_DIR = "outputs/part_a"
GIF_DIR = os.path.join(OUTPUT_DIR, "gifs")
PLOT_PATH = os.path.join(OUTPUT_DIR, "baseline_stats.png")
SUCCESS_REWARD_THRESHOLD = 200.0
ACTION_DIM = 4


def run_random_baseline(num_episodes: int = NUM_EPISODES) -> dict:
    env = gym.make(ENV_NAME)

    state_dim = env.observation_space.shape[0]
    action_dim = env.action_space.n
    print(f"Env ID: {env.spec.id}")
    print(f"State dimension: {state_dim}")
    print(f"Action dimension: {action_dim}")

    episode_rewards = []
    episode_lengths = []
    successes = 0

    for episode in range(1, num_episodes + 1):
        state, _ = env.reset()
        done = False
        episode_reward = 0.0
        episode_length = 0

        while not done:
            # Random baseline policy:
            # select one valid action uniformly from the environment's action space.
            action = env.action_space.sample()
            next_state, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated

            episode_reward += reward
            episode_length += 1
            state = next_state

        episode_rewards.append(episode_reward)
        episode_lengths.append(episode_length)

        # For Part A, treat a very strong total episode reward as a "success".
        if episode_reward >= SUCCESS_REWARD_THRESHOLD:
            successes += 1

        if episode % 10 == 0 or episode == 1:
            print(
                f"Episode {episode:3d}/{num_episodes} | "
                f"Reward: {episode_reward:8.2f} | "
                f"Length: {episode_length:4d}"
            )

    env.close()

    stats = {
        "episode_rewards": episode_rewards,
        "episode_lengths": episode_lengths,
        "mean_reward": float(np.mean(episode_rewards)),
        "std_reward": float(np.std(episode_rewards)),
        "min_reward": float(np.min(episode_rewards)),
        "max_reward": float(np.max(episode_rewards)),
        "mean_length": float(np.mean(episode_lengths)),
        "success_rate": successes / num_episodes,
    }
    return stats


def main() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Run the random baseline first so we can measure how bad uninformed behavior is.
    stats = run_random_baseline()
    print()
    print_stats(stats)
    plot_baseline(stats, out_path=PLOT_PATH)

    print()
    print(f"Recording {NUM_RECORD_EPISODES} random-policy episodes...")
    # Use a single helper call to save a few baseline GIFs.
    record_episodes(
        num_episodes=NUM_RECORD_EPISODES,
        out_dir=GIF_DIR,
        # This policy ignores the state and picks one of the 4 actions at random.
        policy_fn=lambda state: np.random.randint(0, ACTION_DIM),
    )

    print()
    print("Part A baseline complete.")
    print(f"Plot saved to: {PLOT_PATH}")
    print(f"GIFs saved to: {GIF_DIR}")


if __name__ == "__main__":
    main()
