# baseline Summary

## Run Info

- Algorithm: Vanilla DQN
- Requested device: cpu
- Actual device: cpu
- Train episodes: 650
- Evaluation episodes: 100
- Duration: 00:14:55
- Solved at: 596

## Hyperparameters

| Parameter | Value |
| --- | --- |
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
| mean_reward | 133.41 |
| std_reward | 90.85 |
| min_reward | -22.15 |
| max_reward | 299.47 |
| mean_length | 286.9 |
| success_rate | 30.0% |
