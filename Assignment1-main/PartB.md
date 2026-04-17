# Part B Guide

## Goal

Part B is where you build the actual learning agent.

Unlike Part A, the agent should no longer act randomly all the time.
It should begin learning from experience and improve over episodes.

For this assignment, the most natural Part B solution is a **DQN agent**.

## What You Need To Deliver

By the end of Part B, you should have:

- a Q-network
- a replay buffer
- an agent class or equivalent logic
- epsilon-greedy action selection
- a target network
- a training loop that runs for at least `500` episodes
- saved checkpoints

## Big Idea Of Part B

The DQN agent learns from transitions:

```text
(state, action, reward, next_state, done)
```

Each time the agent interacts with the environment:

1. it chooses an action
2. it gets the next state and reward
3. it stores that experience
4. it later trains on a random batch of stored experiences

This is much more stable than learning only from the most recent step.

## Step 1: Decide The Core Structure

Your `main.py` should eventually have these pieces:

- environment setup
- Q-network class
- replay buffer class
- agent class
- training loop
- evaluation code

You do not need a perfect architecture.
You do need a clean one.

## Step 2: Build The Q-Network

The Q-network takes the current state as input and predicts one Q-value for each action.

### Input

- state vector of size `8`

### Output

- one Q-value for each of the `4` actions

### Simple architecture

A good beginner architecture is:

```text
8 -> hidden layer -> hidden layer -> 4
```

Example:

- Linear(8, 128)
- ReLU
- Linear(128, 128)
- ReLU
- Linear(128, 4)

### What it means

If the network outputs:

```text
[-1.3, 0.2, 1.8, 0.5]
```

then action `2` is currently considered best.

## Step 3: Build The Replay Buffer

The replay buffer stores past transitions.

Each stored item should contain:

- `state`
- `action`
- `reward`
- `next_state`
- `done`

### What the buffer should do

- `push(...)`: store a transition
- `sample(batch_size)`: return a random minibatch
- `__len__()`: return current size

### Why it matters

Without replay, consecutive samples are too similar.
That makes neural network training unstable.

## Step 4: Create The Agent

Your agent should hold:

- `q_network`
- `target_network`
- `optimizer`
- `replay_buffer`
- `gamma`
- `batch_size`

The agent should also provide methods like:

- `select_action(state, epsilon)`
- `store_transition(...)`
- `train_step()`
- `update_target_network()`

You can use different method names if you want, but the responsibilities should stay clear.

## Step 5: Implement Epsilon-Greedy Action Selection

This is how the agent balances exploration and exploitation.

### Rule

- with probability `epsilon`, choose a random action
- otherwise, choose the action with the highest predicted Q-value

### Pseudocode

```python
if random.random() < epsilon:
    action = env.action_space.sample()
else:
    action = argmax(Q(state))
```

### Why this matters

Early in training:

- high epsilon
- more exploration

Later in training:

- lower epsilon
- more exploitation of learned behavior

## Step 6: Create The Target Network

This is a second copy of the Q-network.

### Important rule

- the online network is updated often
- the target network is updated only sometimes

### Why this matters

If the same network is used to both predict and define the target every time, learning can become unstable.

So the target network gives a more stable reference.

### Common approach

Every `N` episodes:

```python
target_network.load_state_dict(q_network.state_dict())
```

## Step 7: Implement The Training Step

This is the most important part of Part B.

### Before training

Only train if the replay buffer has enough samples:

```python
if len(replay_buffer) < batch_size:
    return
```

### Training flow

1. sample a minibatch from replay memory
2. convert the batch to tensors
3. compute current Q-values for the chosen actions
4. compute target Q-values using the target network
5. compute the loss
6. backpropagate
7. update the online Q-network

### DQN target

For non-terminal transitions:

```text
target = reward + gamma * max_a' Q_target(next_state, a')
```

For terminal transitions:

```text
target = reward
```

### Loss

A practical default is:

- `nn.SmoothL1Loss()` also called Huber loss

It is commonly used in DQN because it is usually more stable than plain MSE.

## Step 8: Build The Training Loop

The loop in `main.py` should eventually do this:

1. reset the environment
2. choose actions using epsilon-greedy
3. step the environment
4. store transitions in replay memory
5. call `train_step()`
6. accumulate episode reward
7. end the episode when `terminated or truncated`
8. decay epsilon after the episode
9. save statistics
10. periodically update the target network

### What to track each episode

- total reward
- average loss
- epsilon
- average Q-value

These tracked values will be used in Part C for plots.

## Step 9: Save Checkpoints

You already have a helper in `utils.py`:

- `save_checkpoint(agent, episode, rewards, filename)`

Use it every `50` to `100` episodes.

Why:

- training can take time
- experiments can crash
- you may want to resume later

## Step 10: Minimum Working Version First

Do not try to build an advanced DQN immediately.

Your first working Part B version should only aim for:

- correct environment interaction
- correct replay buffer usage
- correct Q-learning update
- correct target network sync
- correct epsilon decay

After that, you can improve things.

## Suggested Order For Coding Part B

Follow this order:

1. create the Q-network class
2. create the replay buffer class
3. create the agent class
4. implement `select_action`
5. implement `train_step`
6. copy weights into the target network once at initialization
7. complete the training loop
8. add metric tracking
9. add checkpoint saving

## Common Mistakes In Part B

### Environment mistakes

- forgetting `done = terminated or truncated`
- forgetting that `reset()` returns `(state, info)`

### Tensor mistakes

- wrong tensor shapes
- wrong tensor dtypes
- not adding batch dimensions when needed
- forgetting to move from NumPy arrays to tensors

### DQN mistakes

- training before the replay buffer is large enough
- forgetting to gather the Q-value of the chosen action
- computing targets with the wrong network
- not masking terminal states
- forgetting to detach target values from gradient flow
- updating the target network too often or never

### Training loop mistakes

- not decaying epsilon
- not tracking rewards
- overwriting values incorrectly
- not saving checkpoints

## Definition Of Done

Part B is done when all of these are true:

- [ ] the Q-network runs on a state input
- [ ] the replay buffer stores and samples transitions
- [ ] the agent can choose actions with epsilon-greedy
- [ ] the training step computes targets and loss correctly
- [ ] the target network updates periodically
- [ ] the training loop runs for at least `500` episodes
- [ ] checkpoints are saved during training
- [ ] `main.py` is ready to generate metrics for Part C

## What Comes After Part B

After Part B, Part C will focus on:

- plotting reward curves
- monitoring loss
- monitoring epsilon
- monitoring Q-values
- evaluating the trained policy
- recording learned-agent behavior

Part B is where the agent learns.
Part C is where you prove and analyze that learning.
