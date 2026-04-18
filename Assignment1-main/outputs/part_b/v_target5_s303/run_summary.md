# v_target5_s303 Summary

## Run Info

- Algorithm: Vanilla DQN
- Seed: 303
- Requested device: cpu
- Actual device: cpu
- Train episodes: 650
- Evaluation episodes: 100
- Duration: 00:36:33
- Solved at: 498

## Hyperparameters

| Parameter | Value |
| --- | --- |
| seed | 303 |
| learning_rate | 0.0005 |
| gamma | 0.99 |
| epsilon_start | 1.0 |
| epsilon_end | 0.01 |
| epsilon_decay | 0.995 |
| batch_size | 64 |
| buffer_size | 10000 |
| target_update_freq | 5 |
| num_episodes | 650 |
| eval_episodes | 100 |
| hidden_dim | 128 |
| success_reward_threshold | 200.0 |
| max_steps_per_episode | 500 |

## Evaluation Stats

| Metric | Value |
| --- | --- |
| mean_reward | 214.02 |
| std_reward | 107.34 |
| min_reward | -99.03 |
| max_reward | 301.80 |
| mean_length | 238.0 |
| success_rate | 76.0% |
