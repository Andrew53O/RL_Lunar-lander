# Part B Guide

## Goal

Part B is where you implement the actual learning agent.

In Part A, the lander acted randomly.
In Part B, the lander should begin learning from experience by using **Vanilla DQN**.

This part is mainly about:

- building the DQN pieces correctly
- making the training loop stable enough to run
- avoiding common bugs that waste time later

## What You Need To Deliver

By the end of Part B, you should have:

- a Q-network
- a replay buffer
- a DQN agent
- epsilon-greedy action selection
- a target network
- a working training loop
- checkpoints saved during training

## Big Idea Of Part B

The agent learns from transitions:

```text
(state, action, reward, next_state, done)
```

Each step of training should follow this pattern:

1. observe the current state
2. choose an action
3. step the environment
4. store the transition
5. sample old experiences from replay memory
6. update the Q-network

The goal is not to hard-code a landing policy.
The goal is to let the network learn which actions lead to better long-term reward.

## Step 1: Keep The Main Structure Simple

Your `main.py` should still look like the starter file:

- imports
- hyperparameters
- environment creation
- classes for the agent
- training loop
- testing / evaluation section

That keeps the assignment readable and easier to explain.

## Step 2: Build The Q-Network

The Q-network is the neural network that estimates:

```text
Q(state, action)
```

That means:

- input: one state vector of size `8`
- output: one Q-value for each of the `4` actions

### Simple architecture

A clean default architecture is:

```text
8 -> 128 -> 128 -> 4
```

with `ReLU` activations between layers.

### What the output means

If the network outputs:

```text
[-1.3, 0.2, 1.8, 0.5]
```

then action `2` is the highest-valued action according to the current model.

## Step 3: Build The Replay Buffer

The replay buffer stores old transitions:

- `state`
- `action`
- `reward`
- `next_state`
- `done`

### Why replay is important

If the agent only learns from the newest step, the data is too correlated.

Replay helps by:

- mixing old and new experiences
- stabilizing neural network training
- improving sample efficiency

### Minimum replay buffer methods

- `push(...)`
- `sample(batch_size)`
- `__len__()`

## Step 4: Create The DQN Agent

The agent should contain:

- `q_network`
- `target_network`
- `optimizer`
- `loss_fn`
- `replay_buffer`

The agent should also provide methods like:

- `select_action(state, epsilon)`
- `greedy_action(state)`
- `store_transition(...)`
- `train_step()`
- `update_target_network()`

## Step 5: Use Epsilon-Greedy Action Selection

The agent must balance:

- exploration
- exploitation

### Rule

- with probability `epsilon`, choose a random action
- otherwise, choose the greedy action from the Q-network

### Why this matters

At the beginning:

- the network knows almost nothing
- exploration is necessary

Later:

- the network should rely more on what it has learned

That is why epsilon usually starts near `1.0` and decays over time.

## Step 6: Add The Target Network

The target network is a delayed copy of the online Q-network.

### Why it matters

If the online network is used both:

- to predict current Q-values
- and to define target Q-values

then learning can become unstable.

The target network reduces that instability by changing more slowly.

### Common pattern

Every few episodes:

```python
target_network.load_state_dict(q_network.state_dict())
```

## Step 7: Implement The DQN Training Step

This is the core update rule.

### Before training

Do not train until the replay buffer has enough samples:

```python
if len(replay_buffer) < batch_size:
    return
```

### Main training flow

1. sample a minibatch
2. convert arrays to tensors
3. compute the current Q-value for the chosen action
4. compute the target Q-value
5. compute loss
6. backpropagate
7. update the online network

### Standard DQN target

For non-terminal transitions:

```text
target = reward + gamma * max_a' Q_target(next_state, a')
```

For terminal transitions:

```text
target = reward
```

### Recommended loss

Use:

- `nn.SmoothL1Loss()`

This is also called Huber loss and is a common default for DQN.

## Step 8: Build The Training Loop

The training loop should:

1. reset the environment
2. choose actions using epsilon-greedy
3. step the environment
4. store transitions
5. run `train_step()`
6. accumulate episode reward
7. stop when the episode ends
8. decay epsilon
9. update the target network periodically
10. save metrics and checkpoints

Track at least:

- episode reward
- average loss
- epsilon
- mean Q-value

## Step 9: Solve The Long-Episode Hover Problem

This is one of the most practical problems in Part B.

### What you observed

Sometimes after many episodes, the lander does not crash or land quickly.
Instead, it:

- drifts in the air
- hovers badly
- keeps flying for a long time

This makes one episode take much longer than the others.

### Why this happens

This usually means the agent has learned a **partial policy**:

- it avoids immediate crashing
- but it has not learned to finish the landing

So it survives without solving the task.

This is not unusual in reinforcement learning.
It means the policy is learning something, but not enough yet.

### Why it slows training

The training loop only moves to the next episode after the current one ends.

So if one episode drags on too long, then:

- training progress slows down
- one bad hover policy wastes time

### Practical solution

Use a manual episode step cap.

Example:

```python
MAX_STEPS_PER_EPISODE = 500
```

Then inside the loop:

```python
episode_steps += 1
if episode_steps >= MAX_STEPS_PER_EPISODE:
    done = True
```

### Why this is a good fix

- it prevents one episode from taking too long
- it makes training time more predictable
- it keeps the code simple
- it is practical for assignments and experiments

### Important note

If you use a custom step cap in training, use the same idea in evaluation too, so comparisons stay fair.

## Step 10: Save Checkpoints

Save checkpoints every `50` to `100` episodes.

Why:

- training takes time
- runs may crash
- you may want to compare runs later

This is also useful for Part C and Part D.

## Step 11: What A Good First Version Looks Like

A good first Part B implementation does **not** need to be fancy.

It should simply be:

- correct
- readable
- stable enough to train

You do not need advanced DQN improvements yet.
Vanilla DQN is enough for a good first implementation.

## Suggested Coding Order

Follow this order:

1. Q-network
2. replay buffer
3. agent class
4. epsilon-greedy action selection
5. training step
6. target network update
7. training loop
8. manual episode step cap
9. checkpoints
10. metric tracking

## Common Mistakes In Part B

### Environment mistakes

- forgetting `done = terminated or truncated`
- forgetting that `reset()` returns `(state, info)`

### Tensor mistakes

- wrong tensor shape in `gather`
- wrong dtype for actions
- forgetting batch dimensions
- forgetting to convert NumPy arrays to tensors

### DQN mistakes

- training before replay memory is ready
- using the wrong network for targets
- not handling terminal states correctly
- forgetting target-network updates
- epsilon not decaying

### Training-loop mistakes

- not tracking episode reward
- not saving checkpoints
- not capping very long episodes
- assuming long survival always means good learning

## Definition Of Done

Part B is done when all of these are true:

- [ ] the Q-network runs correctly
- [ ] the replay buffer stores and samples transitions
- [ ] the agent can choose actions with epsilon-greedy
- [ ] the training step computes Q-targets and loss correctly
- [ ] the target network updates periodically
- [ ] the training loop runs end to end
- [ ] checkpoints are saved
- [ ] very long hover/drift episodes are capped
- [ ] Part C metrics can be collected from the run

## What Comes After Part B

After Part B, Part C is about:

- plotting reward, loss, epsilon, and Q-values
- evaluating the learned policy
- comparing results to the random baseline
- recording learned-agent behavior

Part B is where the agent learns.
Part C is where you prove and analyze that learning.
