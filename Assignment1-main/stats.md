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
| 2026-04-18 18:30:46 | ddqn_baseline3 | Double DQN | random | 650 | 100 | cpu | cpu | 00:46:37 | Not solved | 164.59 | 0.0005 | 0.995 | 10 |
| 2026-04-18 18:28:43 | v_base_s202 | Vanilla DQN | 202 | 650 | 100 | cpu | cpu | 00:42:29 | Not solved | 180.32 | 0.0005 | 0.995 | 10 |
| 2026-04-18 18:31:33 | v_base_s101 | Vanilla DQN | 101 | 650 | 100 | cpu | cpu | 00:45:48 | 606 | 213.00 | 0.0005 | 0.995 | 10 |
| 2026-04-18 18:32:40 | v_base_s303 | Vanilla DQN | 303 | 650 | 100 | cpu | cpu | 00:46:10 | 649 | 202.12 | 0.0005 | 0.995 | 10 |
| 2026-04-18 18:35:20 | v_eps993_s202 | Vanilla DQN | 202 | 650 | 100 | cpu | cpu | 00:46:57 | 613 | 217.88 | 0.0005 | 0.993 | 10 |
| 2026-04-18 18:35:56 | v_eps993_s101 | Vanilla DQN | 101 | 650 | 100 | cpu | cpu | 00:48:17 | 608 | 198.31 | 0.0005 | 0.993 | 10 |
| 2026-04-18 18:36:36 | v_eps993_s303 | Vanilla DQN | 303 | 650 | 100 | cpu | cpu | 00:47:41 | 630 | 196.87 | 0.0005 | 0.993 | 10 |
| 2026-04-18 19:00:59 | v_eps997_s101 | Vanilla DQN | 101 | 650 | 100 | cpu | cpu | 00:31:29 | Not solved | 117.66 | 0.0005 | 0.997 | 10 |
| 2026-04-18 19:06:15 | v_eps997_s303 | Vanilla DQN | 303 | 650 | 100 | cpu | cpu | 00:31:19 | Not solved | 181.10 | 0.0005 | 0.997 | 10 |
| 2026-04-18 19:06:50 | v_eps997_s202 | Vanilla DQN | 202 | 650 | 100 | cpu | cpu | 00:32:17 | Not solved | 174.58 | 0.0005 | 0.997 | 10 |
| 2026-04-18 19:12:28 | v_target5_s202 | Vanilla DQN | 202 | 650 | 100 | cpu | cpu | 00:35:14 | 511 | 180.02 | 0.0005 | 0.995 | 5 |
| 2026-04-18 19:13:59 | v_target5_s101 | Vanilla DQN | 101 | 650 | 100 | cpu | cpu | 00:37:14 | 596 | 215.83 | 0.0005 | 0.995 | 5 |
| 2026-04-18 19:14:10 | v_target5_s303 | Vanilla DQN | 303 | 650 | 100 | cpu | cpu | 00:36:33 | 498 | 214.02 | 0.0005 | 0.995 | 5 |
| 2026-04-18 19:38:07 | v_target20_s202 | Vanilla DQN | 202 | 650 | 100 | cpu | cpu | 00:30:04 | Not solved | 167.01 | 0.0005 | 0.995 | 20 |
| 2026-04-18 19:41:08 | v_target20_s101 | Vanilla DQN | 101 | 650 | 100 | cpu | cpu | 00:33:27 | Not solved | 153.67 | 0.0005 | 0.995 | 20 |
| 2026-04-18 19:41:54 | v_target20_s303 | Vanilla DQN | 303 | 650 | 100 | cpu | cpu | 00:33:41 | Not solved | 128.02 | 0.0005 | 0.995 | 20 |
| 2026-04-18 20:01:25 | v_lr2p5e4_s101 | Vanilla DQN | 101 | 650 | 100 | cpu | cpu | 00:36:50 | 608 | 211.62 | 0.00025 | 0.995 | 10 |
| 2026-04-18 20:01:32 | v_lr2p5e4_s202 | Vanilla DQN | 202 | 650 | 100 | cpu | cpu | 00:36:48 | Not solved | 194.20 | 0.00025 | 0.995 | 10 |
| 2026-04-18 20:03:11 | v_lr2p5e4_s303 | Vanilla DQN | 303 | 650 | 100 | cpu | cpu | 00:38:07 | Not solved | 184.71 | 0.00025 | 0.995 | 10 |
| 2026-04-18 20:09:13 | v_lr1e3_s202 | Vanilla DQN | 202 | 650 | 100 | cpu | cpu | 00:23:24 | Not solved | 140.97 | 0.001 | 0.995 | 10 |
| 2026-04-18 20:10:56 | v_lr1e3_s101 | Vanilla DQN | 101 | 650 | 100 | cpu | cpu | 00:25:09 | Not solved | 151.28 | 0.001 | 0.995 | 10 |
| 2026-04-18 20:21:22 | v_lr1e3_s303 | Vanilla DQN | 303 | 650 | 100 | cpu | cpu | 00:12:19 | Not solved | 22.10 | 0.001 | 0.995 | 10 |
