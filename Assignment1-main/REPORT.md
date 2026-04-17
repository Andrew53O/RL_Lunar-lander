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
