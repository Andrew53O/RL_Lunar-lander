# v_base_s101 Summary

## Run Info

- Algorithm: Vanilla DQN
- Seed: 101
- Requested device: cpu
- Actual device: cpu
- Train episodes: 650
- Evaluation episodes: 100
- Duration: 00:45:48
- Solved at: 606

## Hyperparameters

| Parameter | Value |
| --- | --- |
| seed | 101 |
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
| mean_reward | 213.00 |
| std_reward | 67.97 |
| min_reward | -20.87 |
| max_reward | 306.76 |
| mean_length | 311.8 |
| success_rate | 68.0% |
