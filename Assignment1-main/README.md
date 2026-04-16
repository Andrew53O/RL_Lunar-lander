# CSE727 Reinforcement Learning Assignment 1

## Lunar Lander

This assignment asks us to build a reinforcement learning agent for `LunarLander-v3` in Gymnasium. The main goal is to train an agent that can land the spacecraft safely between the two flags, control its angle and speed, and do so efficiently enough to achieve a strong reward.

The assignment is not only about making the agent run. It also requires us to:

- understand the environment and its state/action spaces
- implement a value-based RL agent
- train and evaluate the agent
- visualize learning behaviour
- compare hyperparameter settings
- write a short report about the results

According to the assignment slides, the environment is considered solved when the **average reward is greater than 200 over 100 consecutive episodes**.

## What This Repository Contains

- `main.py`: starter code for building and training the RL agent
- `utils.py`: helper functions for recording videos/GIFs, printing statistics, plotting results, and saving/loading checkpoints
- `requirements.txt`: required Python packages for the assignment
- `assignment1_lunar_lander_arl_slides.pdf`: the assignment brief and grading requirements

## Assignment Objective

The problem to solve is:

> Build an agent for `LunarLander-v3` that learns a landing policy which brings the spacecraft safely to rest between two flags while using thrust efficiently.

This assignment is designed to combine several important reinforcement learning ideas in one practical task:

- environment interaction
- states, actions, rewards, and episodes
- exploration vs. exploitation
- neural network value approximation
- experience replay
- target networks
- training analysis and debugging

## Environment Summary

`LunarLander-v3` has:

- **State space: 8 dimensions**
  - x and y position
  - x and y velocity
  - angle and angular velocity
  - left leg contact
  - right leg contact
- **Action space: 4 discrete actions**
  - `0`: do nothing
  - `1`: fire left orientation engine
  - `2`: fire main engine
  - `3`: fire right orientation engine

The lander starts near the top of the screen with random initial motion, so the agent must learn to:

- stabilize its orientation
- reduce descent speed
- move toward the landing pad
- land softly without crashing

## Possible Algorithms

The assignment slides state that **all algorithms are acceptable**, which means the project is not limited to only one RL method. However, because this repository uses `LunarLander-v3` with a **discrete action space**, some algorithms are a much better fit than others.

### Algorithms that can be used

| Algorithm | Type | Fits `LunarLander-v3` well? | Notes |
| --- | --- | --- | --- |
| Q-Learning | Value-based | Yes, with discretization | Simple idea, but the continuous state space makes pure tabular use difficult. |
| SARSA | Value-based | Yes, with discretization | Similar to Q-Learning, but learns on-policy. |
| Expected SARSA | Value-based | Yes, with discretization | A smoother extension of SARSA. |
| Monte Carlo Control | Value-based | Possible | Can be used, but often less practical for this task than temporal-difference methods. |
| DQN | Deep value-based | Yes | The most natural choice for this starter code. |
| Double DQN | Deep value-based | Yes | Improves DQN by reducing overestimation bias. |
| Dueling DQN | Deep value-based | Yes | Often improves value estimation by separating state value and advantage. |
| Prioritized Replay DQN | Deep value-based | Yes | Extends DQN by sampling more useful experiences more often. |
| n-step DQN | Deep value-based | Yes | Can improve learning speed by using multi-step returns. |
| Rainbow-style DQN | Deep value-based | Yes | Combines several DQN improvements, but is more complex to implement. |
| REINFORCE | Policy-based | Yes | Valid, but usually less stable and sample-efficient than DQN-based methods here. |
| Actor-Critic | Policy/value hybrid | Yes | A valid alternative to DQN. |
| A2C | Policy/value hybrid | Yes | Works with discrete actions and is commonly used. |
| A3C | Policy/value hybrid | Yes | Valid, but more complex because of asynchronous training. |
| PPO | Policy/value hybrid | Yes | Strong and popular algorithm for discrete control tasks. |

### Best choices for this assignment

If the goal is to stay close to the provided starter code, the most practical choices are:

- `DQN`
- `Double DQN`
- `Dueling DQN`

These fit the assignment requirements especially well because the slides explicitly mention ideas such as:

- neural-network Q-function approximation
- experience replay
- target network updates
- epsilon-greedy exploration

Those are all core parts of the DQN family.

### Less suitable algorithms

Some RL algorithms are usually designed for **continuous action spaces**, so they are not a direct match for `LunarLander-v3`:

- `DDPG`
- `TD3`
- `SAC`

These are better suited to `LunarLanderContinuous-v3`, not the discrete version used in this assignment.

## What `main.py` Does

`main.py` is the main starter file for the assignment. Right now it is a template and still contains several `TODO` sections.

It already includes:

- package imports for Gymnasium, NumPy, PyTorch, and plotting
- core hyperparameters such as learning rate, discount factor, epsilon schedule, batch size, replay buffer size, and target update frequency
- creation of the `LunarLander-v3` environment
- automatic reading of:
  - `state_dim` from the observation space
  - `action_dim` from the action space
- a training loop skeleton over `1000` episodes
- placeholders for testing the trained agent

### What still needs to be implemented in `main.py`

Based on the code skeleton and the assignment brief, `main.py` is where we are expected to add the main RL solution:

1. **Agent components**
   - Q-network
   - target network
   - replay buffer
   - optimizer and loss function

2. **Action selection**
   - epsilon-greedy policy
   - random exploration at the beginning
   - greedy action selection from the network during exploitation

3. **Training logic**
   - store transitions `(state, action, reward, next_state, done)`
   - sample mini-batches from replay memory
   - compute target Q-values
   - optimize the online Q-network
   - periodically update the target network

4. **Bookkeeping**
   - decay epsilon after each episode
   - track episode rewards
   - print progress during training
   - save useful metrics for later plotting

5. **Evaluation**
   - run the trained agent without exploration
   - measure final performance
   - optionally record episodes for submission

In short, `main.py` is the file where the actual reinforcement learning agent must be implemented and trained.

## What `utils.py` Does

`utils.py` provides helper utilities for the assignment. It does not contain the agent itself, but it supports the experiments, evaluation, and submission artifacts.

### Main helper functions in `utils.py`

- `make_env_with_video(...)`
  - creates a `LunarLander-v3` environment with Gymnasium video recording enabled
  - useful for saving videos during training

- `record_episodes(num_episodes, out_dir, policy_fn)`
  - runs episodes using a provided policy function
  - saves each episode as a GIF
  - useful for baseline videos and trained-agent demonstrations

- `print_stats(stats)`
  - prints a clean summary of mean reward, standard deviation, min/max reward, average episode length, and success rate

- `moving_average(data, window=20)`
  - smooths noisy training curves
  - especially useful for reward, loss, and Q-value plots

- `plot_baseline(stats, out_path=...)`
  - generates plots for the random-policy baseline
  - includes reward trend, reward distribution, episode length trend, and a summary panel

- `plot_training_curves(metrics, out_dir=...)`
  - generates a 2x2 training dashboard
  - plots:
    - episode rewards
    - training loss
    - epsilon decay
    - mean max Q-values

- `save_checkpoint(agent, episode, rewards, filename)`
  - saves model parameters, optimizer state, and reward history

- `load_checkpoint(agent, filename)`
  - restores a saved checkpoint into an agent

### Why `utils.py` matters

The assignment is not graded only on code correctness. We also need evidence that the agent was trained, analyzed, and evaluated properly. `utils.py` helps produce exactly those outputs:

- statistics summaries
- plots
- checkpoints
- videos or GIFs

## What We Need to Solve

The assignment can be understood as four parts.

### Part A: Environment Setup and Baseline

We need to:

- install Gymnasium and create the `LunarLander-v3` environment
- implement a random-policy baseline
- run `100` episodes
- compute:
  - mean reward
  - episode length
  - success rate
- save `3` to `5` episode recordings as videos or GIFs

Expected outputs:

- random baseline code
- baseline statistics
- baseline plots
- sample recordings

### Part B: Agent Implementation

We need to implement the main RL agent. The slides say all algorithms are acceptable, but the starter code and utilities strongly suggest a DQN-style solution.

Required components include:

- neural-network Q-function approximator
- experience replay buffer
- target network with periodic updates
- epsilon-greedy exploration
- training loop for at least `500` episodes

Expected outputs:

- complete agent implementation
- working training loop
- saved model checkpoints

### Part C: Training and Analysis

After implementing the agent, we need to train and analyze it.

We need to:

- track rewards during training
- monitor epsilon decay
- monitor loss values
- monitor average Q-values
- plot learning curves with moving averages
- evaluate the trained policy for `100` no-exploration episodes
- record `3` to `5` test episodes of learned behaviour

Expected outputs:

- training plots
- test performance statistics
- videos or GIFs of the learned agent

### Part D: Experimentation and Report

We also need to do controlled experiments and explain the results.

The slides require at least **3 hyperparameter variations**. Suggested settings to explore include:

- learning rate
- batch size
- epsilon decay
- network depth/width
- target update frequency
- replay buffer size

The written report should discuss questions such as:

- How does epsilon decay affect learning speed and final performance?
- What happens if the target network is updated too often or too rarely?
- Which hyperparameter mattered most?
- What failure modes were observed during training?
- How does the learned policy compare with intuition about good landing behaviour?

Expected outputs:

- comparison plots
- written report of about `2` to `3` pages

## Expected Submission Package

From the assignment PDF, the final submission should include:

- all Python source files (`.py`)
- trained model weights (`.pt` or `.pth`)
- plots and figures (`.png` or `.pdf`)
- `3` to `5` videos or GIFs showing agent behaviour
- written report (`.pdf`)

## Recommended Workflow

A practical way to complete this assignment is:

1. Run the environment and confirm the state/action dimensions.
2. Implement the random baseline and collect Part A statistics.
3. Build the DQN agent in `main.py`.
4. Add replay buffer, target network, and epsilon-greedy action selection.
5. Train for at least `500` episodes.
6. Save checkpoints and training metrics.
7. Use `utils.py` to generate plots and videos.
8. Evaluate the final model over `100` test episodes.
9. Run at least `3` hyperparameter experiments.
10. Write the final report summarizing results and insights.

## Installation

Create a Python environment and install the dependencies:

```bash
pip install -r requirements.txt
```

Main packages used in this assignment:

- `gymnasium[box2d]`
- `torch`
- `numpy`
- `matplotlib`
- `imageio`
- `tqdm`

## Current Status of This Starter Code

At the moment, this repository is a **starter template**, not a finished solution.

- `main.py` still has important `TODO` sections
- `utils.py` is mostly ready and provides supporting tools
- the README now explains the assignment requirements and the intended implementation work

## Summary

This assignment is about building, training, evaluating, and analyzing an RL agent for `LunarLander-v3`.

The core thing we need to solve is:

- create an agent that learns a strong landing policy
- support it with proper training logic and stability mechanisms
- show the results through plots, statistics, and videos
- compare hyperparameters and explain the findings in a report

In this repository:

- `main.py` is where the actual agent and training logic should be implemented
- `utils.py` is where the helper tools for analysis, plotting, recording, and checkpoints are provided
