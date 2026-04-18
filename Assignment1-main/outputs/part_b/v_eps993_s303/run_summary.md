# v_eps993_s303 Summary

## Run Info

- Algorithm: Vanilla DQN
- Seed: 303
- Requested device: cpu
- Actual device: cpu
- Train episodes: 650
- Evaluation episodes: 100
- Duration: 00:47:41
- Solved at: 630

## Hyperparameters

| Parameter | Value |
| --- | --- |
| seed | 303 |
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
| mean_reward | 196.87 |
| std_reward | 82.69 |
| min_reward | -34.81 |
| max_reward | 287.40 |
| mean_length | 312.7 |
| success_rate | 61.0% |
