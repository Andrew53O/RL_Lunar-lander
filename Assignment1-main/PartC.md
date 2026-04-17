# Part C Guide

## Goal

Part C is about showing that the agent is actually learning and then evaluating how well it performs.

Part B is where you build the DQN agent.
Part C is where you **measure**, **visualize**, and **explain** what happened during training.

You are not only training the model here.
You are collecting evidence.

## What You Need To Deliver

By the end of Part C, you should have:

- training reward history
- loss history
- epsilon history
- mean Q-value history
- training plots
- evaluation results over `100` no-exploration episodes
- `3` to `5` recorded test episodes of the learned agent

## Big Idea Of Part C

Part C answers questions like:

- Is the reward getting better over time?
- Is the agent learning stably or unstably?
- Is exploration decreasing as expected?
- Are Q-values behaving reasonably?
- Does the trained agent perform better than the random baseline?

This is the part where you show the difference between:

- "the code runs"
- and
- "the agent learned something meaningful"

## Step 1: Track The Right Metrics During Training

During each episode, record:

- total episode reward
- average training loss for that episode
- epsilon value
- average max Q-value for that episode

These should be stored in lists across all episodes.

### Why these metrics matter

#### Episode reward

This is the most important performance signal.

- if it increases over time, the agent is likely improving
- if it stays very negative, the agent may not be learning

#### Training loss

This shows how well the Q-network is fitting the target values.

- noisy loss is normal
- very large or exploding loss may be a warning sign
- low loss alone does not guarantee good behavior

#### Epsilon

This tells you how much the agent is exploring.

- early training: high epsilon
- later training: lower epsilon

If epsilon does not decrease correctly, the agent may keep behaving too randomly.

#### Mean max Q-value

This is a rough measure of how large the network’s predicted best Q-values are.

It helps you spot:

- no learning at all
- unstable value growth
- strange value collapse

## Step 2: Plot The Training Curves

Use `plot_training_curves(metrics, out_dir=...)` from `utils.py`.

The expected metrics dictionary is:

```python
metrics = {
    "episode_rewards": ...,
    "avg_losses": ...,
    "epsilons": ...,
    "mean_q_values": ...,
    "solved_at": ...,
}
```

The plot should include:

- reward curve
- loss curve
- epsilon decay
- mean Q-value curve

### Why plots matter

Raw episode values are noisy.

Plots help you see:

- long-term trends
- instability
- plateaus
- whether training improved compared with the baseline

## Step 3: Use Moving Averages

Training in reinforcement learning is noisy.

That means raw reward curves often jump up and down a lot.

Moving averages help reveal the trend underneath the noise.

Why this matters:

- a single good episode does not mean the policy is good
- a single bad episode does not mean the training failed
- the moving average gives a more stable view of learning

## Step 4: Understand The Solved Criterion

The assignment uses this condition:

- average reward greater than `200` over `100` consecutive episodes

This is not about one lucky episode.

It means the agent must perform well **consistently** over many episodes.

In code, this usually means:

```python
np.mean(rewards_history[-100:]) > 200
```

If this happens for the first time, store that episode index in:

- `solved_at`

## Step 5: Evaluate The Final Trained Agent

After training is finished, evaluate the agent with **no exploration**.

That means:

- do not use random epsilon actions
- always choose the greedy action from the Q-network

Run evaluation for:

- `100` episodes

Track:

- mean reward
- standard deviation
- minimum reward
- maximum reward
- mean episode length
- success rate

### Why no-exploration evaluation matters

During training, the agent is partly random because of epsilon-greedy exploration.

For final evaluation, you want to measure what the learned policy actually does when it is fully exploiting what it learned.

## Step 6: Compare Part C Against Part A

A very important goal in Part C is to compare your trained DQN agent with the random baseline from Part A.

Look for improvement in:

- average reward
- success rate
- landing stability
- visual behavior in recorded episodes

Expected comparison:

- random baseline: poor, unstable, mostly negative rewards
- trained DQN: better rewards, more controlled movement, more successful landings

## Step 7: Record 3 To 5 Learned-Agent Episodes

Use the learned policy to record:

- `3` to `5` test episodes

These recordings are useful because they show:

- whether the lander is stable
- whether it uses thrust intentionally
- whether it lands softly
- whether the visual behavior matches the reward improvement

This is important because sometimes numbers improve while behavior still looks strange.

## Step 8: Save Outputs Clearly

Suggested output structure:

```text
outputs/
  part_b_c/
    training_curves.png
    checkpoints/
      dqn_episode_100.pt
      dqn_episode_200.pt
      ...
      dqn_final.pt
```

If you later record learned-agent GIFs, you can place them in:

```text
outputs/
  part_b_c/
    gifs/
```

## Step 9: What Good Training Usually Looks Like

Common healthy signs:

- rewards improve over time
- moving-average reward trends upward
- epsilon decreases steadily
- loss stays finite
- Q-values change over time instead of staying flat
- evaluation is clearly better than the random baseline

Common warning signs:

- rewards stay flat and very negative
- loss becomes `nan`
- Q-values explode to unrealistic values
- the agent never improves visually
- evaluation is no better than random

## Step 10: How To Interpret Each Plot

### Reward plot

Ask:

- Is the trend going upward?
- Is the moving average improving?
- Does the curve plateau early?

### Loss plot

Ask:

- Is the loss finite?
- Is it extremely unstable?
- Does it become more controlled over time?

### Epsilon plot

Ask:

- Does epsilon decay smoothly?
- Is the exploration schedule behaving as expected?

### Q-value plot

Ask:

- Are the Q-values changing over time?
- Are they growing in a believable way?
- Are they exploding or collapsing?

## Step 11: Write Down Observations For The Report

As soon as Part C is finished, write notes in `REPORT.md`.

Useful observations:

- whether reward improved compared with Part A
- whether training was noisy or stable
- whether epsilon decay seemed too fast or too slow
- whether the loss behaved reasonably
- whether the learned behavior looked controlled in recorded episodes
- whether the final evaluation looked convincing

These notes will make Part D much easier later.

## Common Mistakes In Part C

- only reporting one reward number without plots
- forgetting to store all metrics over time
- evaluating with epsilon still active
- confusing training performance with evaluation performance
- claiming success from one lucky episode
- not comparing against the random baseline
- not recording learned-agent episodes

## Definition Of Done

Part C is done when all of these are true:

- [ ] reward history is saved
- [ ] loss history is saved
- [ ] epsilon history is saved
- [ ] mean Q-value history is saved
- [ ] training curves are plotted
- [ ] solved criterion is checked
- [ ] final evaluation runs for `100` no-exploration episodes
- [ ] evaluation stats are printed and saved for report use
- [ ] `3` to `5` learned-agent episodes are recorded
- [ ] observations are written into `REPORT.md`

## What Comes After Part C

After Part C, Part D will ask you to compare different hyperparameter settings.

That means Part C gives you the evidence for one training run, while Part D compares several training runs and explains:

- what changed
- what improved
- what became worse
- which hyperparameter mattered most

So Part C is the foundation for Part D.
