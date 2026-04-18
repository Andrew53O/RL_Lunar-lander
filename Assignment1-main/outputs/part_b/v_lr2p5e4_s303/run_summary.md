# v_lr2p5e4_s303 Summary

## Run Info

- Algorithm: Vanilla DQN
- Seed: 303
- Requested device: cpu
- Actual device: cpu
- Train episodes: 650
- Evaluation episodes: 100
- Duration: 00:38:07
- Solved at: Not solved

## Hyperparameters

| Parameter | Value |
| --- | --- |
| seed | 303 |
| learning_rate | 0.00025 |
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
| mean_reward | 184.71 |
| std_reward | 79.52 |
| min_reward | 38.71 |
| max_reward | 295.56 |
| mean_length | 366.0 |
| success_rate | 61.0% |
