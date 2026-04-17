# Part A Guide

## Goal

Part A is about setting up the `LunarLander-v3` environment and building a **random-policy baseline**.

You are not trying to make the agent smart yet.
You are trying to:

- confirm the environment works
- understand the state and action spaces
- collect baseline statistics
- save baseline plots
- record a few example episodes

## What You Need To Deliver

By the end of Part A, you should have:

- code that creates the environment
- code that runs a random agent for `100` episodes
- summary statistics
- a baseline plot
- `3` to `5` recorded episodes as GIFs or videos

## Step 1: Install Dependencies

Since you are using a virtual environment called `myenv` inside **WSL**, do the setup from the WSL terminal, not from Windows Python.

Recommended commands:

```bash
cd Assignment1-main
source ../myenv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If your `myenv` folder is inside `Assignment1-main` instead of the parent folder, use:

```bash
cd Assignment1-main
source myenv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

After activation, verify that WSL is using the venv correctly:

```bash
which python
which pip
python --version
```

The `python` and `pip` paths should point to `myenv`.

Then install the required packages:

```bash
pip install -r requirements.txt
```

Important note:

- `gymnasium[box2d]` is required for `LunarLander-v3`
- if `gymnasium` is missing, the code will not run
- in WSL, always install packages after activating `myenv`
- avoid mixing WSL Python with Windows Python

## Step 2: Confirm The Environment Works

Before writing the baseline, make sure you can create the environment.

What to check:

- the environment name is `LunarLander-v3`
- the observation space has `8` values
- the action space has `4` discrete actions

What you should print:

- `state_dim`
- `action_dim`

Expected result:

- `state_dim = 8`
- `action_dim = 4`

## Step 3: Understand The Environment

Before running experiments, know what the state and actions mean.

### State meaning

The `8` state values are:

- x position
- y position
- x velocity
- y velocity
- angle
- angular velocity
- left leg contact
- right leg contact

### Action meaning

The `4` actions are:

- `0`: do nothing
- `1`: fire left engine
- `2`: fire main engine
- `3`: fire right engine

### Baseline intuition

A random agent chooses actions without thinking.

So the baseline will usually:

- crash often
- waste fuel
- get poor rewards
- show unstable behavior

That is normal.
The point of the baseline is to give you something to compare against later.

## Step 4: Create A Random Policy

The simplest baseline policy is:

```python
action = env.action_space.sample()
```

This means the agent chooses a random valid action at each step.

## Step 5: Run 100 Episodes

Run the random policy for `100` episodes.

For each episode, track:

- total reward
- episode length in steps
- whether the landing was successful

Inside each episode:

1. reset the environment
2. choose random actions until the episode ends
3. accumulate the reward
4. count the steps
5. store the final episode statistics

Important Gymnasium detail:

```python
state, _ = env.reset()
next_state, reward, terminated, truncated, _ = env.step(action)
done = terminated or truncated
```

## Step 6: Compute Baseline Statistics

After `100` episodes, compute:

- mean reward
- standard deviation of reward
- minimum reward
- maximum reward
- mean episode length
- success rate

### Suggested meaning of success rate

For Part A, use a simple and consistent rule.

A practical default is:

- count an episode as success if total reward is greater than or equal to `200`

This is simple for the random baseline, even though true successful landings will likely be very rare.

Store the results in a dictionary like this:

```python
stats = {
    "episode_rewards": episode_rewards,
    "episode_lengths": episode_lengths,
    "mean_reward": ...,
    "std_reward": ...,
    "min_reward": ...,
    "max_reward": ...,
    "mean_length": ...,
    "success_rate": ...,
}
```

This matches what `utils.py` expects.

## Step 7: Print And Plot The Results

Use the helpers from `utils.py`:

- `print_stats(stats)`
- `plot_baseline(stats, out_path=...)`

The baseline plot should help you answer:

- how bad is the random policy?
- how noisy are the rewards?
- how long do episodes usually last?
- does the random agent ever get close to success?

## Step 8: Record 3 To 5 Example Episodes

Use the helper:

- `record_episodes(num_episodes, out_dir, policy_fn)`

For the baseline policy, pass a random action function.

Example idea:

```python
policy_fn=lambda state: env.action_space.sample()
```

Purpose of these recordings:

- show what random behavior looks like
- provide visual evidence for your report
- make later comparison with the trained agent easier

## Step 9: Organize The Output Files

It will help a lot if you keep Part A outputs in one place.

Suggested structure:

```text
outputs/
  part_a/
    baseline_stats.png
    episode_1.gif
    episode_2.gif
    ...
```

## Step 10: Write Down Observations

As soon as you finish Part A, write a few notes in `THOUGHTS.md`.

Useful observations:

- average reward range
- whether episode lengths are short or long
- whether the random agent ever lands safely
- what the motion looks like in the recordings
- why the random baseline is a useful comparison point

These notes will help later when writing the final report.

## Common Mistakes In Part A

- using the wrong environment name
- forgetting to install `gymnasium[box2d]`
- forgetting that `reset()` returns `(state, info)`
- forgetting that `done = terminated or truncated`
- not storing episode rewards and lengths
- not using the correct keys expected by `plot_baseline(...)`
- recording too many videos and wasting disk space

## Definition Of Done

Part A is done when all of these are true:

- [ ] the environment runs without import errors
- [ ] you confirmed state dimension `8`
- [ ] you confirmed action dimension `4`
- [ ] the random baseline ran for `100` episodes
- [ ] you computed the required statistics
- [ ] you printed the summary
- [ ] you saved the baseline plot
- [ ] you recorded `3` to `5` episodes
- [ ] you saved short notes about what happened

## What Comes After Part A

After Part A, the next stage is Part B:

- implement the DQN agent
- create the replay buffer
- create the Q-network
- add epsilon-greedy action selection
- add target-network updates

For now, Part A is only about setup and the random baseline.
