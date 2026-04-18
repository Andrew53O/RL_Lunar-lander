# lr1e3 Summary

## Run Info

- Algorithm: Vanilla DQN
- Requested device: cpu
- Actual device: cpu
- Train episodes: 650
- Evaluation episodes: 100
- Duration: 00:24:04
- Solved at: Not solved

## Hyperparameters

| Parameter | Value |
| --- | --- |
| learning_rate | 0.001 |
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
| mean_reward | 91.59 |
| std_reward | 156.08 |
| min_reward | -555.42 |
| max_reward | 286.62 |
| mean_length | 265.7 |
| success_rate | 26.0% |
