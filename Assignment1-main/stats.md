# Run Stats

Each completed training run appends one row here.

`Seed = random` means the run used uncontrolled system randomness because fixed seed support had not been added yet.

| Run Time | Run | Algorithm | Seed | Train Episodes | Eval Episodes | Requested Device | Actual Device | Duration | Solved At | Eval Mean Reward | LR | Epsilon Decay | Target Update |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-04-18 14:13:23 | run1 | Vanilla DQN | random | 550 | 100 | auto | cuda | 00:29:12 | Not solved | 172.52 | 5e-4 | 0.995 | 10 |
| 2026-04-18 15:05:36 | run2 | Vanilla DQN | random | 650 | 100 | auto | cuda | 00:25:21 | 610 | 217.21 | 5e-4 | 0.995 | 10 |
| 2026-04-18 15:40:59 | eps997 | Vanilla DQN | random | 650 | 100 | cpu | cpu | 00:11:23 | Not solved | 180.91 | 0.0005 | 0.997 | 10 |
| 2026-04-18 15:42:52 | eps993 | Vanilla DQN | random | 650 | 100 | cpu | cpu | 00:14:56 | Not solved | 199.18 | 0.0005 | 0.993 | 10 |
| 2026-04-18 16:19:02 | baseline | Vanilla DQN | random | 650 | 100 | cpu | cpu | 00:14:55 | 596 | 133.41 | 0.0005 | 0.995 | 10 |
| 2026-04-18 16:21:31 | target5 | Vanilla DQN | random | 650 | 100 | cpu | cpu | 00:14:13 | Not solved | 198.01 | 0.0005 | 0.995 | 5 |
| 2026-04-18 16:46:25 | baseline2 | Vanilla DQN | random | 650 | 100 | cpu | cpu | 00:22:55 | 618 | 182.46 | 0.0005 | 0.995 | 10 |
| 2026-04-18 16:46:55 | target20 | Vanilla DQN | random | 650 | 100 | cpu | cpu | 00:23:03 | Not solved | 155.35 | 0.0005 | 0.995 | 20 |
| 2026-04-18 16:48:37 | lr2p5e4 | Vanilla DQN | random | 650 | 100 | cpu | cpu | 00:24:28 | Not solved | 139.93 | 0.00025 | 0.995 | 10 |
| 2026-04-18 17:13:55 | baseline3 | Vanilla DQN | random | 650 | 100 | cpu | cpu | 00:25:34 | Not solved | 187.83 | 0.0005 | 0.995 | 10 |
| 2026-04-18 17:14:48 | target5-2 | Vanilla DQN | random | 650 | 100 | cpu | cpu | 00:23:12 | Not solved | 181.90 | 0.0005 | 0.995 | 5 |
| 2026-04-18 17:16:14 | lr1e3 | Vanilla DQN | random | 650 | 100 | cpu | cpu | 00:24:04 | Not solved | 91.59 | 0.001 | 0.995 | 10 |
| 2026-04-18 17:21:32 | ddqn_baseline1 | Double DQN | random | 650 | 100 | cpu | cpu | 00:24:42 | Not solved | 186.85 | 0.0005 | 0.995 | 10 |
| 2026-04-18 17:26:01 | target5-3 | Vanilla DQN | random | 650 | 100 | cpu | cpu | 00:11:10 | Not solved | 104.61 | 0.0005 | 0.995 | 5 |
| 2026-04-18 17:40:55 | ddqn_baseline2 | Double DQN | random | 650 | 100 | cpu | cpu | 00:13:52 | 644 | 212.09 | 0.0005 | 0.995 | 10 |
