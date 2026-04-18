# v_lr1e3_s101 Summary

## Run Info

- Algorithm: Vanilla DQN
- Seed: 101
- Requested device: cpu
- Actual device: cpu
- Train episodes: 650
- Evaluation episodes: 100
- Duration: 00:25:09
- Solved at: Not solved

## Hyperparameters

| Parameter | Value |
| --- | --- |
| seed | 101 |
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
| mean_reward | 151.28 |
| std_reward | 97.14 |
| min_reward | -58.79 |
| max_reward | 278.43 |
| mean_length | 352.0 |
| success_rate | 42.0% |
