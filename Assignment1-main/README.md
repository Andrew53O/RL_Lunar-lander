# Folder Structure Guide

This folder only includes a smaller submission set of trained model weights, plot figures, and GIF files.

For the complete project version, please visit:

- https://github.com/Andrew53O/RL_Lunar-lander

This README only describes these parts of the assignment folder:

- `main.py`
- `main_random.py`
- `outputs/`

It intentionally does **not** document other files here, and it also skips:

- `outputs/launcher_logs/`
- `outputs/part_ddqn/`

## `main.py`

`main.py` is the main Vanilla DQN training script for `LunarLander-v3`.

What it does:

- creates the environment
- builds the Q-network and target network
- uses a replay buffer
- trains with epsilon-greedy exploration
- saves checkpoints during training
- evaluates the final greedy policy for `100` episodes
- writes training outputs into `outputs/part_b/`
- appends run results into `stats.md`

Main default hyperparameters in this file:

- `LEARNING_RATE = 5e-4`
- `GAMMA = 0.99`
- `EPSILON_START = 1.0`
- `EPSILON_END = 0.01`
- `EPSILON_DECAY = 0.995`
- `BATCH_SIZE = 64`
- `BUFFER_SIZE = 10000`
- `TARGET_UPDATE_FREQ = 10`
- `NUM_EPISODES = 650`
- `CHECKPOINT_FREQ = 50`
- `EVAL_EPISODES = 100`
- `HIDDEN_DIM = 128`
- `SUCCESS_REWARD_THRESHOLD = 200.0`
- `MAX_STEPS_PER_EPISODE = 500`

Important CLI overrides supported by `main.py`:

- `--device`
- `--run-name`
- `--learning-rate`
- `--epsilon-decay`
- `--target-update-freq`
- `--batch-size`
- `--num-episodes`
- `--max-steps-per-episode`
- `--seed`

The naming of many run folders inside `outputs/part_b/` comes directly from these CLI arguments.

## `main_random.py`

`main_random.py` is the Part A random baseline script.

What it does:

- runs `100` random-policy episodes
- computes mean reward, standard deviation, min/max reward, mean episode length, and success rate
- saves the baseline plot into `outputs/part_a/`
- records `5` random-policy GIFs into `outputs/part_a/gifs/`

This file is used as the non-learning reference point before the DQN experiments.

## `outputs/`

The `outputs/` folder stores generated results from training, plotting, and recording.

This README documents:

- `outputs/part_a/`
- `outputs/part_b/`
- `outputs/report_figures/`
- `outputs/report_gifs/`

It does **not** document:

- `outputs/launcher_logs/`
- `outputs/part_ddqn/`

---

## `outputs/part_a/`

This folder contains the random baseline outputs from `main_random.py`.

Contents:

- `baseline_stats.png`
  - the plot created from the random baseline statistics

- `gifs/`
  - the recorded random-policy GIFs for Part A

---

## `outputs/part_b/`

This folder contains the Vanilla DQN experiment runs from `main.py`.

Each run folder usually contains:

- `checkpoints/`
  - saved model checkpoints such as `dqn_episode_100.pt` and `dqn_final.pt`

- `training_curves.png`
  - the 2x2 training summary plot produced by `plot_training_curves(...)`

- `run_summary.md`
  - a short markdown summary of:
    - algorithm
    - seed
    - device
    - training episodes
    - evaluation episodes
    - solved episode
    - hyperparameters
    - evaluation statistics

For the smaller submission-ready set, some selected run folders also contain renamed files such as:

- `v_base_s101_training_curves.png`
- `v_base_s101_dqn_episode_650.pt`

These renamed files are easier to identify when only a few trained weights and plots are being submitted.

### Naming pattern of seeded run folders

Many folders follow this style:

- `v_<experiment>_s<seed>`

Where:

- `v` means Vanilla DQN
- the middle part describes which hyperparameter changed
- `s101`, `s202`, or `s303` means the seed value

Examples:

- `v_base_s101`
  - Vanilla DQN baseline setting with seed `101`

- `v_base_s202`
  - Vanilla DQN baseline setting with seed `202`

- `v_base_s303`
  - Vanilla DQN baseline setting with seed `303`

- `v_eps993_s101`
  - Vanilla DQN run where `EPSILON_DECAY` was changed to `0.993` with seed `101`

- `v_eps993_s202`
  - Vanilla DQN run where `EPSILON_DECAY` was changed to `0.993` with seed `202`

- `v_eps993_s303`
  - Vanilla DQN run where `EPSILON_DECAY` was changed to `0.993` with seed `303`

- `v_eps997_s101`
  - Vanilla DQN run where `EPSILON_DECAY` was changed to `0.997` with seed `101`

- `v_eps997_s202`
  - Vanilla DQN run where `EPSILON_DECAY` was changed to `0.997` with seed `202`

- `v_eps997_s303`
  - Vanilla DQN run where `EPSILON_DECAY` was changed to `0.997` with seed `303`

- `v_target5_s101`
  - Vanilla DQN run where `TARGET_UPDATE_FREQ` was changed to `5` with seed `101`

- `v_target5_s202`
  - Vanilla DQN run where `TARGET_UPDATE_FREQ` was changed to `5` with seed `202`

- `v_target5_s303`
  - Vanilla DQN run where `TARGET_UPDATE_FREQ` was changed to `5` with seed `303`

- `v_target20_s101`
  - Vanilla DQN run where `TARGET_UPDATE_FREQ` was changed to `20` with seed `101`

- `v_target20_s202`
  - Vanilla DQN run where `TARGET_UPDATE_FREQ` was changed to `20` with seed `202`

- `v_target20_s303`
  - Vanilla DQN run where `TARGET_UPDATE_FREQ` was changed to `20` with seed `303`

- `v_lr2p5e4_s101`
  - Vanilla DQN run where `LEARNING_RATE` was changed to `0.00025` with seed `101`

- `v_lr2p5e4_s202`
  - Vanilla DQN run where `LEARNING_RATE` was changed to `0.00025` with seed `202`

- `v_lr2p5e4_s303`
  - Vanilla DQN run where `LEARNING_RATE` was changed to `0.00025` with seed `303`

- `v_lr1e3_s101`
  - Vanilla DQN run where `LEARNING_RATE` was changed to `0.001` with seed `101`

- `v_lr1e3_s202`
  - Vanilla DQN run where `LEARNING_RATE` was changed to `0.001` with seed `202`

- `v_lr1e3_s303`
  - Vanilla DQN run where `LEARNING_RATE` was changed to `0.001` with seed `303`

### `outputs/part_b/1.uncontrolable/`

This folder stores the earlier uncontrolled experiments from before the fixed-seed comparison workflow was finalized.

These runs are useful as history, but they are not the main controlled experiment set used in the final seeded comparison.

Inside it are folders such as:

- `baseline`, `baseline2`, `baseline3`
  - earlier baseline runs without the later fixed-seed structure

- `eps993`, `eps997`
  - earlier epsilon-decay experiments

- `target5`, `target5-2`, `target5-3`, `target20`
  - earlier target-update experiments

- `lr2p5e4`, `lr1e3`
  - earlier learning-rate experiments

- `run1`, `run2`
  - older automatically named training runs from before the later explicit naming scheme

---

## `outputs/report_figures/`

This folder contains the final report-ready comparison figures.

Current files:

- `epsilon_decay_comparison.png`
  - compares final evaluation performance for `EPSILON_DECAY = 0.993`, `0.995`, and `0.997`

- `epsilon_schedule_curves.png`
  - shows the exploration-probability schedules for `0.993`, `0.995`, and `0.997`

- `target_update_comparison.png`
  - compares final evaluation performance for `TARGET_UPDATE_FREQ = 5`, `10`, and `20`

- `learning_rate_comparison.png`
  - compares final evaluation performance for `LEARNING_RATE = 0.00025`, `0.0005`, and `0.001`

These images were created for use in the report and are based on the seeded Vanilla DQN runs.

---

## `outputs/report_gifs/`

This folder contains the selected GIFs for the report.

Current files:

- `good_1_epsilon_decay_0.993.gif`
  - a good example from the `EPSILON_DECAY = 0.993` setting

- `good_2_target_update_5.gif`
  - a good example from the `TARGET_UPDATE_FREQ = 5` setting

- `normal_1_baseline.gif`
  - a normal baseline example

- `bad_1_epsilon_decay_0.997.gif`
  - a weak example from the `EPSILON_DECAY = 0.997` setting

- `bad_2_learning_rate_0.001.gif`
  - a weak example from the `LEARNING_RATE = 0.001` setting

- `selection_summary.md`
  - a summary file that lists:
    - category
    - source run
    - reward
    - GIF filename
