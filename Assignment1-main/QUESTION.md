# Questions and Answers

## Q1. What does `SUCCESS_REWARD_THRESHOLD = 200` mean, and how does the LunarLander reward system work?

`200` is **not** a distance.

It is a **reward score** given by the environment.

You can think of reward like a game score:

- good behavior adds points
- bad behavior removes points
- the final episode reward is the total score for the whole landing attempt

So when we write:

```python
SUCCESS_REWARD_THRESHOLD = 200.0
```

it means:

- if the total episode score is `200` or more, we count that episode as a strong success

It does **not** mean:

- 200 meters
- 200 steps
- 200 pixels

It means:

- a total performance score of `200`

The environment gives reward based on things like:

- moving toward the landing pad
- reducing speed
- staying upright
- touching down with the legs
- landing successfully
- not wasting too much fuel
- avoiding crashes

So `200` is a benchmark score for very good behavior over a whole episode.

### Q1.1 How does the environment decide that score?

The environment decides it through its built-in **reward function**.

It does not "understand" like a human.
It simply calculates a score from the lander's behavior at each step.

At every step:

- the current state is measured
- a reward or penalty is computed
- that value is added into the episode total

At the end:

- all step rewards are summed
- that total becomes the `episode_reward`

So a high score means the behavior was good according to the environment's rules, while a low or negative score means the behavior was poor.

### Q1.2 What is the actual reward formula in `LunarLander-v3`?

From the installed Gymnasium environment, the reward shaping is:

```python
shaping = (
    -100 * sqrt(state[0]^2 + state[1]^2)
    -100 * sqrt(state[2]^2 + state[3]^2)
    -100 * abs(state[4])
    +10 * state[6]
    +10 * state[7]
)
```

Then the reward for each step is computed as:

```python
reward = shaping - prev_shaping
reward -= 0.30 * m_power
reward -= 0.03 * s_power
```

And terminal rewards are:

```python
if crash or out_of_bounds:
    reward = -100

if landed_and_sleeping:
    reward = +100
```

### Q1.3 What does each term in the formula mean?

#### Position penalty

```python
-100 * sqrt(state[0]^2 + state[1]^2)
```

This penalizes being far from the landing pad.

- `state[0]`: horizontal offset
- `state[1]`: vertical offset

If the lander is far from the target area, this term becomes more negative.

#### Velocity penalty

```python
-100 * sqrt(state[2]^2 + state[3]^2)
```

This penalizes moving too fast.

- `state[2]`: horizontal velocity
- `state[3]`: vertical velocity

Fast movement is dangerous, so the environment reduces reward.

#### Angle penalty

```python
-100 * abs(state[4])
```

This penalizes tilt.

- `state[4]`: lander angle

If the lander is not upright, the score becomes worse.

#### Leg contact reward

```python
+10 * state[6] + 10 * state[7]
```

This rewards ground contact with the legs.

- `state[6]`: left leg contact
- `state[7]`: right leg contact

Each touching leg adds positive reward.

#### Fuel cost

```python
reward -= 0.30 * m_power
reward -= 0.03 * s_power
```

This penalizes engine use.

- `m_power`: main engine usage
- `s_power`: side engine usage

This encourages efficient control rather than wasting fuel.

#### Crash penalty and landing bonus

```python
if crash or out_of_bounds:
    reward = -100

if landed_and_sleeping:
    reward = +100
```

- crashing gives a large negative reward
- successful rest gives a large positive reward

### Q1.4 Why is the reward still hard to understand?

Because reward is not one physical measurement.

It is not:

- distance only
- speed only
- angle only

Instead, it combines many factors into one total score.

So reward is more like an overall performance grade for the whole landing attempt.

### Q1.5 What is the most important idea in the formula?

This line is the key idea:

```python
reward = shaping - prev_shaping
```

This means the environment mostly rewards **improvement**.

So the agent gets rewarded when it becomes:

- closer to the landing pad
- slower
- more upright
- better positioned to land

And it gets punished when it becomes:

- farther away
- faster
- more tilted
- more unstable

So the reward is not just:

> "How good is the state right now?"

It is more like:

> "Did the new state become better or worse than the previous one?"

### Q1.6 Why does a random agent usually fail to reach `200`?

A random agent does not coordinate its actions.

That means it often:

- fires engines at the wrong time
- tilts too much
- moves away from the landing pad
- falls too fast
- wastes fuel
- crashes

Because of this, the total episode reward is usually low or negative.

Reaching `200` normally requires:

- controlled descent
- good balance
- correct horizontal adjustment
- soft landing
- efficient engine usage

That is why `200` is a strong success threshold.
