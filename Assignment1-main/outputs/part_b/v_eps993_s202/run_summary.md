# v_eps993_s202 Summary

## Run Info

- Algorithm: Vanilla DQN
- Seed: 202
- Requested device: cpu
- Actual device: cpu
- Train episodes: 650
- Evaluation episodes: 100
- Duration: 00:46:57
- Solved at: 613

## Hyperparameters

| Parameter | Value |
| --- | --- |
| seed | 202 |
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
| mean_reward | 217.88 |
| std_reward | 72.51 |
| min_reward | 47.66 |
| max_reward | 297.82 |
| mean_length | 315.8 |
| success_rate | 74.0% |
