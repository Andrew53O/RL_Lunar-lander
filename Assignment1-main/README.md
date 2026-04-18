# CSE727 Assignment 1: LunarLander

This repository contains my working solution and experiment files for `LunarLander-v3` using Gymnasium.

The project currently includes:

- a Part A random baseline runner
- a Vanilla DQN trainer in `main.py`
- a Double DQN trainer in `main_ddqn.py`
- a multiprocessing launcher for running many experiment commands
- notes and report files for Parts A to D

According to the assignment brief, the environment is considered solved when the average reward over `100` consecutive training episodes is greater than `200`.

## Environment Summary

`LunarLander-v3` has:

- observation space: `8` values
- action space: `4` discrete actions
  - `0`: do nothing
  - `1`: fire left orientation engine
  - `2`: fire main engine
  - `3`: fire right orientation engine

## Current Important Files

### Training and evaluation

- `main.py`
  - current Vanilla DQN training script
  - supports seeded and unseeded runs
  - supports CLI hyperparameter overrides
  - writes outputs to `outputs/part_b/`

- `main_ddqn.py`
  - Double DQN version of the trainer
  - same overall structure as `main.py`
  - writes outputs to `outputs/part_ddqn/`

- `main_random.py`
  - Part A random baseline script
  - runs `100` random-policy episodes
  - saves baseline plots and GIFs under `outputs/part_a/`

- `main_multiprocessing.py`
  - launcher for running multiple experiment commands in parallel
  - reads commands from `COMMANDS.md`
  - runs unchecked jobs by default
  - writes launcher logs to `outputs/launcher_logs/`

### Utilities

- `utils.py`
  - helper functions for:
    - plotting baseline statistics
    - plotting training curves
    - printing evaluation statistics
    - saving checkpoints
    - recording GIFs

- `requirements.txt`
  - Python dependencies for the project

### Experiment tracking and writing

- `stats.md`
  - global run history
  - records algorithm, seed, timing, solved episode, evaluation reward, and selected hyperparameters

- `COMMANDS.md`
  - checklist of seeded experiment commands
  - each command has its own copyable code block

- `REPORT.md`
  - current report draft focused on the seeded `main.py` hyperparameter experiments

- `QUESTION.md`
  - Q&A notes collected while working on the assignment

- `PartA.md`, `PartB.md`, `PartC.md`, `PartD.md`
  - step-by-step working notes for each assignment part


### Assignment brief

- `assignment1_lunar_lander_arl_slides.pdf`
  - the assignment PDF/slides

## Current `main.py` Configuration

These are the default hyperparameters currently defined in `main.py`:

| Hyperparameter | Value |
| --- | --- |
| `LEARNING_RATE` | `5e-4` |
| `GAMMA` | `0.99` |
| `EPSILON_START` | `1.0` |
| `EPSILON_END` | `0.01` |
| `EPSILON_DECAY` | `0.995` |
| `BATCH_SIZE` | `64` |
| `BUFFER_SIZE` | `10000` |
| `TARGET_UPDATE_FREQ` | `10` |
| `NUM_EPISODES` | `650` |
| `CHECKPOINT_FREQ` | `50` |
| `EVAL_EPISODES` | `100` |
| `HIDDEN_DIM` | `128` |
| `SUCCESS_REWARD_THRESHOLD` | `200.0` |
| `MAX_STEPS_PER_EPISODE` | `500` |

The Q-network structure in `main.py` is:

- `8 -> 128 -> 128 -> 4`
- `ReLU` activations

The script currently supports these CLI overrides:

- `--device`
- `--run-name`
- `--learning-rate`
- `--epsilon-decay`
- `--target-update-freq`
- `--batch-size`
- `--num-episodes`
- `--max-steps-per-episode`
- `--seed`

## Current `main_ddqn.py` Configuration

`main_ddqn.py` currently mirrors the same default hyperparameters as `main.py`, but changes the training target to Double DQN:

- the online network selects the best next action
- the target network evaluates that selected action

This file is intended for comparison against the Vanilla DQN baseline.

## Output Structure

### Part A outputs

- `outputs/part_a/baseline_stats.png`
- `outputs/part_a/gifs/`

### Vanilla DQN outputs

- `outputs/part_b/<run_name>/training_curves.png`
- `outputs/part_b/<run_name>/checkpoints/`
- `outputs/part_b/<run_name>/run_summary.md`

### Double DQN outputs

- `outputs/part_ddqn/<run_name>/training_curves.png`
- `outputs/part_ddqn/<run_name>/checkpoints/`
- `outputs/part_ddqn/<run_name>/run_summary.md`

### Launcher outputs

- `outputs/launcher_logs/`

## How to Run

Activate the virtual environment first if needed.

Example:

```bash
source ../myenv/bin/activate
```

### Part A random baseline

```bash
python main_random.py
```

### Vanilla DQN baseline run

```bash
python main.py --device cpu --run-name baseline_seed101 --seed 101
```

### Vanilla DQN hyperparameter override example

```bash
python main.py --device cpu --run-name eps993_seed101 --epsilon-decay 0.993 --seed 101
```

### Double DQN baseline run

```bash
python main_ddqn.py --device cpu --run-name ddqn_seed101 --seed 101
```

### Multiprocessing experiment launcher

```bash
python main_multiprocessing.py --max-workers 2
```

Useful launcher options:

```bash
python main_multiprocessing.py --dry-run
python main_multiprocessing.py --max-workers 2
python main_multiprocessing.py --run-names v_lr2p5e4_s101 v_lr2p5e4_s202
```

## Current Experiment Workflow

The current controlled-comparison workflow is:

1. define seeded commands in `COMMANDS.md`
2. run them either manually or with `main_multiprocessing.py`
3. let each run append to `stats.md`
4. inspect each run folder’s `run_summary.md`
5. compare seeded results in `REPORT.md`

Older runs in `stats.md` marked with `Seed = random` were exploratory runs from before fixed seed support was added.

## Notes

- `main.py` is now the primary script for the assignment experiments.
- `REPORT.md` currently focuses only on the seeded Vanilla DQN hyperparameter experiments.
- `main_multiprocessing.py` improves convenience, but actual speedup still depends on how many CPUs WSL can access.
