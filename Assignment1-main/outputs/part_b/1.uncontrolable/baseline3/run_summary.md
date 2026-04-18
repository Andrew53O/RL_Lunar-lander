# baseline3 Summary

## Run Info

- Algorithm: Vanilla DQN
- Requested device: cpu
- Actual device: cpu
- Train episodes: 650
- Evaluation episodes: 100
- Duration: 00:25:34
- Solved at: Not solved

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
| mean_reward | 187.83 |
| std_reward | 70.74 |
| min_reward | 58.02 |
| max_reward | 290.01 |
| mean_length | 385.2 |
| success_rate | 58.0% |
