# ddqn_baseline3 Summary

## Run Info

- Algorithm: Double DQN
- Seed: random
- Requested device: cpu
- Actual device: cpu
- Train episodes: 650
- Evaluation episodes: 100
- Duration: 00:46:37
- Solved at: Not solved

## Hyperparameters

| Parameter | Value |
| --- | --- |
| seed | random |
| learning_rate | 0.0005 |
| gamma | 0.99 |
| epsilon_start | 1.0 |
| epsilon_end | 0.01 |
| epsilon_decay | 0.995 |
| batch_size | 64 |
| buffer_size | 10000 |
| target_update_freq | 10 |
| num_episodes | 650 |
| eval_episodes | 100 |
| hidden_dim | 128 |
| success_reward_threshold | 200.0 |
| max_steps_per_episode | 500 |

## Evaluation Stats

| Metric | Value |
| --- | --- |
| mean_reward | 164.59 |
| std_reward | 97.25 |
| min_reward | -223.11 |
| max_reward | 313.96 |
| mean_length | 350.0 |
| success_rate | 50.0% |
