# v_target5_s202 Summary

## Run Info

- Algorithm: Vanilla DQN
- Seed: 202
- Requested device: cpu
- Actual device: cpu
- Train episodes: 650
- Evaluation episodes: 100
- Duration: 00:35:14
- Solved at: 511

## Hyperparameters

| Parameter | Value |
| --- | --- |
| seed | 202 |
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
| mean_reward | 180.02 |
| std_reward | 105.01 |
| min_reward | 0.04 |
| max_reward | 290.97 |
| mean_length | 212.7 |
| success_rate | 56.0% |
