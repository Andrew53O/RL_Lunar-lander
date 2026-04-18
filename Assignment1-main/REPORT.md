# Assignment Report Notes

## Part A: Random Baseline Observations

This section summarizes the results of the Part A random-policy baseline for `LunarLander-v3`.

### 1. Average reward range

After running the random baseline for `100` episodes, the average reward was:

```text
[Fill in your mean reward here]
```

The reward range was:

```text
Min reward: [fill in]
Max reward: [fill in]
Std reward: [fill in]
```

Observation:

The random baseline is expected to produce mostly low or negative rewards because the agent chooses actions without understanding the state of the lander. This means it cannot reliably control direction, speed, or landing angle.

### 2. Episode length

The average episode length was:

```text
[Fill in mean episode length here]
```

Observation:

If episode lengths are short, the random agent is likely crashing quickly.
If episode lengths are long, it may be drifting, wasting fuel, or surviving for a while without landing successfully.
In either case, long episodes do not necessarily mean good performance.

### 3. Whether the random agent ever lands safely

Success rate:

```text
[Fill in success rate here]
```

Observation:

The random agent will usually have a very low success rate, often close to zero. This is expected because safe landing requires coordinated control of vertical thrust, horizontal correction, and rotation, which random actions cannot provide consistently.

### 4. What the motion looks like in the recordings

Observation from recorded baseline episodes:

- the lander often spins or tilts in unstable ways
- thrust is used at the wrong times
- the lander may drift away from the landing pad
- many episodes end in hard crashes
- even when the lander stays alive for a while, the motion looks unplanned and inefficient

Write your own specific notes here after watching the GIFs:

```text
[Describe what you saw in your recorded episodes]
```

### 5. Why the random baseline is a useful comparison point

The random baseline is important because it gives a lower-performance reference point.
Later, when the DQN agent is trained, we can compare:

- whether the average reward improves
- whether successful landings become more common
- whether motion looks more stable and intentional
- whether the agent uses thrust more efficiently

This makes it possible to show that learning actually happened, instead of only saying the final model looks better.

## Short Summary For Part A

The Part A baseline shows how poorly an agent performs when it selects actions at random. The rewards are expected to be low, safe landings are rare, and the recorded behavior should look unstable. This baseline is useful because it gives a clear starting point for comparing the learned agent in later parts of the assignment.

## Notes To Update Later

After you run `main_random.py`, replace the placeholder values above with:

- mean reward
- standard deviation
- min reward
- max reward
- mean episode length
- success rate

You can also expand this file later with:

- Part B implementation notes
- Part C training and evaluation observations
- Part D experiment comparisons

## Part D: Recommended Experiment Order

Since your current baseline can solve the task around episode `610`, a good report-friendly order for experiments is:

1. `EPSILON_DECAY`
2. `TARGET_UPDATE_FREQ`
3. `LEARNING_RATE`

These are good first choices because:

- they strongly affect learning behavior
- they are easy to explain in the report
- they usually produce visible differences in learning speed or stability

### Suggested values to test

| Hyperparameter | Baseline | Lower / Faster | Higher / Slower | Why test this first |
| --- | --- | --- | --- | --- |
| `EPSILON_DECAY` | `0.995` | `0.993` | `0.997` | Directly changes exploration speed and is usually easy to explain |
| `TARGET_UPDATE_FREQ` | `10` | `5` | `20` | Helps study whether target updates are too frequent or too slow |
| `LEARNING_RATE` | `5e-4` | `2.5e-4` | `1e-3` | Shows the tradeoff between slower stable learning and faster unstable learning |

### What to look for

#### `EPSILON_DECAY`

- `0.993`: exploration decreases faster, so the agent may learn faster early but can get stuck sooner
- `0.995`: current baseline reference
- `0.997`: exploration lasts longer, so early learning may be slower but final performance can improve

#### `TARGET_UPDATE_FREQ`

- `5`: target updates more often, which may speed learning but also make it less stable
- `10`: current baseline reference
- `20`: target updates more slowly, which may be more stable but slower to improve

#### `LEARNING_RATE`

- `2.5e-4`: smaller updates, usually safer but slower
- `5e-4`: current baseline reference
- `1e-3`: larger updates, which may learn faster or become unstable

### Suggested Part D workflow

Start with `EPSILON_DECAY` first.

Why:

- it is the easiest to explain
- it is closely tied to exploration vs exploitation
- it often produces clear differences in the curves

After that, move to:

- `TARGET_UPDATE_FREQ`
- then `LEARNING_RATE`

## Part C: Good Analysis Ideas To Reuse

### Solved criterion vs evaluation result

The assignment defines the environment as solved when the average reward over the last `100` training episodes is greater than `200`. This is different from the final evaluation over `100` no-exploration episodes. These two measurements are related, but they are not exactly the same metric.

This means a run can:

- satisfy the training solved criterion at some point
- but still have a lower final evaluation mean reward than another run

This happened in the current experiments. For example:

- `baseline` solved during training at episode `596`, but its final evaluation mean reward was `133.41`
- `run2` solved during training at episode `610`, but its final evaluation mean reward was `217.21`

This is a useful point to mention in the report because it shows that:

- the solved criterion measures training progress over a sliding window
- the final evaluation measures the greedy policy performance after training
- different metrics do not always rank runs in the same order

### Why identical settings can still give different results

Even when the hyperparameters are identical, DQN training is still stochastic. This means two runs with the same settings can produce different rewards, different solved episodes, and different final evaluation scores.

Sources of randomness include:

- random initial neural network weights
- random environment initial conditions
- epsilon-greedy exploration
- random replay buffer sampling
- possible PyTorch and CUDA nondeterminism

This can be seen in the current results:

- `baseline` and `baseline2` used the same settings
- `baseline` solved at episode `596` with evaluation mean reward `133.41`
- `baseline2` solved at episode `618` with evaluation mean reward `182.46`

This is a strong report point because it explains why repeated runs or multiple seeds would give a more stable comparison.

### Why CPU was faster than GPU in this project

In these experiments, CPU runs were faster than CUDA runs even though CUDA was available. This is not an error. It is reasonable for this assignment because:

- the Q-network is small
- the environment simulation is CPU-based
- the code steps one environment at a time
- GPU kernel launch and transfer overhead can dominate when batches are small

This can be seen in the run log:

- `run2` on CUDA took `00:25:21`
- several CPU runs took around `00:14` to `00:23`

A good report sentence is:

> Although CUDA was available, CPU was often faster in this assignment because LunarLander simulation is CPU-bound and the DQN network is small, so the GPU overhead was not fully amortized.

### Why long episodes happen

During training, some agents learn a partial survival behavior where they avoid crashing but do not complete the landing. In that case, the lander may keep hovering or drifting in the sky, which makes one episode take a long time.

This does not mean the agent is performing well. It often means the policy has learned an incomplete behavior:

- it avoids immediate failure
- but it has not yet learned how to finish the task efficiently

Adding a manual step cap is a practical fix because it:

- prevents extremely long episodes
- keeps total runtime more predictable
- avoids wasting training time on unproductive hovering behavior

## Part D: Good Discussion Ideas

### Hyperparameter changes do not guarantee improvement

One important lesson from the experiments is that changing a hyperparameter does not automatically improve DQN performance. Some changes can make learning:

- slower
- less stable
- more sensitive to randomness

That is why a baseline configuration can remain competitive or even outperform some tuned variants.

### A baseline being strong is not a bad result

If the baseline performs as well as or better than several variations, that is still a meaningful result. It suggests the default setting was already a reasonable balance between:

- exploration
- learning speed
- target-network stability

A good report sentence is:

> The baseline configuration remained competitive, and some hyperparameter changes reduced performance rather than improving it. This suggests the default settings were already a reasonable tradeoff between exploration, stability, and learning speed.

### Different metrics may disagree about which run is best

When comparing runs, it is important to state which metric is being used:

- earliest `solved_at`
- highest final evaluation mean reward
- highest success rate
- shortest runtime

For example, one run may solve the environment slightly earlier during training, while another run may achieve a better final evaluation score. This means there is not always a single "best" run unless the comparison metric is clearly defined.

### Current experimental interpretation

Based on the runs completed so far:

- `run2` achieved the strongest final evaluation mean reward among the shown solved runs: `217.21`
- `baseline` solved slightly earlier than `run2`, but its final evaluation score was much lower
- `eps993` and `target5` were close to the `200` evaluation region but did not solve under the training criterion in the shown runs
- `eps997`, `target20`, and `lr2p5e4` were weaker in the current results

This suggests that:

- the original `EPSILON_DECAY = 0.995` was already a reasonable choice
- slowing target updates to `20` hurt performance in the current run
- decreasing the learning rate to `2.5e-4` may have made learning too slow for `650` episodes

These interpretations should still be presented carefully because DQN has high variance, and repeated runs could shift the ranking.

### Limitation to mention in the report

A useful limitation statement is:

> Because DQN training is stochastic, repeated runs with different random seeds would provide a more stable estimate of each hyperparameter setting. Due to time constraints, the experiments were first compared using single runs, so some of the observed differences may partly reflect randomness.

## Controlled Comparison With Seeds

### Why fixed seeds help this assignment

The assignment encourages controlled comparison rather than anecdotal claims from a single run. For that reason, using a small fixed set of seeds across all compared configurations is a better design than letting each run use uncontrolled randomness.

The main benefit is that it makes the comparison fairer:

- each configuration sees the same set of seeded training conditions
- results are reproducible
- differences are more likely to reflect the hyperparameter change instead of pure luck

### How seeds should be used

Seeds should be used as a control variable, not as a hyperparameter to optimize.

That means:

- choose the seed set before looking at results
- use the same seeds for every compared configuration
- average the results across those seeds
- do not search for "good" seeds
- do not pick only lucky runs for reporting

A strong report sentence is:

> Random seed was used for reproducibility and controlled comparison only. It was not treated as a tunable hyperparameter, and model-selection decisions were not based on finding favorable seeds.

### Why the earlier runs are weaker evidence

The earlier runs in `stats.md` are now marked with `Seed = random`. That means those runs were useful for exploration, but they do not form a strict controlled-comparison set because they used uncontrolled randomness.

Therefore, for the final hyperparameter comparison, it is more rigorous to restart the experiment matrix using a fixed seed set such as three predetermined seeds.

### Recommended seeded experiment design

A practical setup for this homework is:

- choose three fixed seeds, for example `101`, `202`, and `303`
- run every compared configuration on all three seeds
- compare the mean performance across those three runs

This keeps the experiment manageable while giving stronger evidence than a single run.

### Suggested wording for the final report

> To avoid anecdotal conclusions from a single run, each configuration was evaluated over three fixed random seeds. The seeds were used only for reproducibility and controlled comparison, not as tunable hyperparameters. Final comparisons were based on average performance across the same seed set for all configurations.
