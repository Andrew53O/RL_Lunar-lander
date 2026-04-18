# v_lr2p5e4_s202 Summary

## Run Info

- Algorithm: Vanilla DQN
- Seed: 202
- Requested device: cpu
- Actual device: cpu
- Train episodes: 650
- Evaluation episodes: 100
- Duration: 00:36:48
- Solved at: Not solved

## Hyperparameters

| Parameter | Value |
| --- | --- |
| seed | 202 |
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
| mean_reward | 194.20 |
| std_reward | 84.88 |
| min_reward | -42.10 |
| max_reward | 296.52 |
| mean_length | 269.5 |
| success_rate | 65.0% |
