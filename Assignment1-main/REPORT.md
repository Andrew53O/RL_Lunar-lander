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
