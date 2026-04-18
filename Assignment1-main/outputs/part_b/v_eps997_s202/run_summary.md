# v_eps997_s202 Summary

## Run Info

- Algorithm: Vanilla DQN
- Seed: 202
- Requested device: cpu
- Actual device: cpu
- Train episodes: 650
- Evaluation episodes: 100
- Duration: 00:32:17
- Solved at: Not solved

## Hyperparameters

| Parameter | Value |
| --- | --- |
| seed | 202 |
| learning_rate | 0.0005 |
| gamma | 0.99 |
| epsilon_start | 1.0 |
| epsilon_end | 0.01 |
| epsilon_decay | 0.997 |
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
| mean_reward | 174.58 |
| std_reward | 58.87 |
| min_reward | -17.28 |
| max_reward | 273.36 |
| mean_length | 411.4 |
| success_rate | 37.0% |
