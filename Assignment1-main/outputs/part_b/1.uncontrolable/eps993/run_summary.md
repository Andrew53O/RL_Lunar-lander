# eps993 Summary

## Run Info

- Algorithm: Vanilla DQN
- Requested device: cpu
- Actual device: cpu
- Train episodes: 650
- Evaluation episodes: 100
- Duration: 00:14:56
- Solved at: Not solved

## Hyperparameters

| Parameter | Value |
| --- | --- |
| learning_rate | 0.0005 |
| gamma | 0.99 |
| epsilon_start | 1.0 |
| epsilon_end | 0.01 |
| epsilon_decay | 0.993 |
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
| mean_reward | 199.18 |
| std_reward | 61.56 |
| min_reward | 45.26 |
| max_reward | 281.18 |
| mean_length | 355.6 |
| success_rate | 55.0% |
