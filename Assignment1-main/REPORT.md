# Hyperparameter Experiment Report for `main.py`

This report focuses only on the seeded hyperparameter experiments for the Vanilla DQN implementation in `main.py`. It does not cover the random baseline or the Double DQN experiments.

## Experiment Setup

The controlled comparison used the same three fixed seeds for each configuration:

- `101`
- `202`
- `303`

These seeds were used only for reproducibility and fair comparison. They were not treated as tunable hyperparameters. All runs used:

- environment: `LunarLander-v3`
- algorithm: Vanilla DQN
- training episodes: `650`
- evaluation episodes: `100`
- device: CPU

The baseline configuration was:

- `LEARNING_RATE = 5e-4`
- `EPSILON_DECAY = 0.995`
- `TARGET_UPDATE_FREQ = 10`

The tested hyperparameter groups were:

1. `EPSILON_DECAY`: `0.993`, `0.995`, `0.997`
2. `TARGET_UPDATE_FREQ`: `5`, `10`, `20`
3. `LEARNING_RATE`: `2.5e-4`, `5e-4`, `1e-3`

## Summary of Results

The table below summarizes the seeded `main.py` runs that were complete at the time of writing.

| Configuration | Seeds completed | Mean eval reward | Solve rate | Notes |
| --- | --- | --- | --- | --- |
| Baseline `eps=0.995, target=10, lr=5e-4` | `3/3` | `198.48` | `2/3` | Strong reference point |
| `EPSILON_DECAY = 0.993` | `3/3` | `204.35` | `3/3` | Best overall balance in current results |
| `EPSILON_DECAY = 0.997` | `3/3` | `157.78` | `0/3` | Too much exploration too late |
| `TARGET_UPDATE_FREQ = 5` | `3/3` | `203.29` | `3/3` | Fastest learning among completed groups |
| `TARGET_UPDATE_FREQ = 20` | `3/3` | `149.57` | `0/3` | Updates were too infrequent |
| `LEARNING_RATE = 2.5e-4` | `3/3` | `196.84` | `1/3` | Stable but slower than expected |
| `LEARNING_RATE = 1e-3` | `2/3` complete | `146.12` on completed runs | `0/2` on completed runs | Appears unstable, but incomplete |

## Averaged Three-Seed Comparison Tables

These tables aggregate the seeded `main.py` runs by averaging the three evaluation runs for each setting. The averages help reduce anecdotal conclusions from any single lucky or unlucky seed.

### Epsilon Decay Table

This table compares how changing the exploration decay rate affected final evaluation reward, variability, episode length, solve frequency, and how often the agent crossed the training solved criterion.

| Setting | Seeds | Avg Reward | Avg Std Reward | Avg Length | Avg Success Rate | Solved Runs | Avg Solved Episode* |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `0.993` | `101, 202, 303` | `204.35` | `75.69` | `319.9` | `67.0%` | `3/3` | `617.0` |
| `0.995 (baseline)` | `101, 202, 303` | `198.48` | `86.17` | `308.9` | `62.3%` | `2/3` | `627.5` |
| `0.997` | `101, 202, 303` | `157.78` | `71.03` | `416.0` | `36.7%` | `0/3` | `Not solved` |

The main pattern is that `0.993` slightly improved average reward over the baseline, while `0.997` clearly hurt both solve rate and final performance. The much longer average episode length for `0.997` is also consistent with the agent spending more time drifting or hovering instead of finishing the landing.

### Target Update Table

This table shows how often the target network should be refreshed. It highlights one of the clearest differences in the whole experiment set.

| Setting | Seeds | Avg Reward | Avg Std Reward | Avg Length | Avg Success Rate | Solved Runs | Avg Solved Episode* |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `5` | `101, 202, 303` | `203.29` | `99.64` | `237.0` | `69.3%` | `3/3` | `535.0` |
| `10 (baseline)` | `101, 202, 303` | `198.48` | `86.17` | `308.9` | `62.3%` | `2/3` | `627.5` |
| `20` | `101, 202, 303` | `149.57` | `85.31` | `390.9` | `40.0%` | `0/3` | `Not solved` |

The best setting here was `5`, which solved all three seeds and reached the solved threshold earlier than the baseline on average. By contrast, `20` performed poorly on every seed, suggesting that targets became too stale when they were updated too rarely.

### Learning Rate Table

This table compares how the optimizer step size affected the final policy quality.

| Setting | Seeds | Avg Reward | Avg Std Reward | Avg Length | Avg Success Rate | Solved Runs | Avg Solved Episode* |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `0.00025` | `101, 202, 303` | `196.84` | `78.11` | `316.1` | `67.0%` | `1/3` | `608.0` |
| `0.0005 (baseline)` | `101, 202, 303` | `198.48` | `86.17` | `308.9` | `62.3%` | `2/3` | `627.5` |
| `0.001` | `101, 202, 303` | `104.78` | `143.00` | `262.3` | `35.0%` | `0/3` | `Not solved` |

The baseline learning rate `0.0005` remained the best overall choice in this group. Lowering it to `0.00025` kept performance fairly close, but raising it to `0.001` caused a major drop in reward and a large increase in reward variability, which is consistent with unstable updates.

`*` Average solved episode is computed only over runs that actually solved during training.

## Effect of Epsilon Decay on Learning Speed Versus Final Performance

`EPSILON_DECAY` controlled how quickly the agent reduced exploration.

- With `0.993`, exploration decreased faster than the baseline.
- With `0.997`, exploration lasted longer than the baseline.

The results suggest that `0.993` gave the best tradeoff in this experiment set:

- mean evaluation reward: `204.35`
- solve rate: `3/3`
- solved episodes: `608`, `613`, `630`

The baseline `0.995` was still strong:

- mean evaluation reward: `198.48`
- solve rate: `2/3`

However, `0.997` performed much worse:

- mean evaluation reward: `157.78`
- solve rate: `0/3`

This indicates that keeping exploration high for too long hurt both learning speed and final policy quality. In other words, the agent kept trying random actions longer than necessary and did not commit quickly enough to a good landing strategy.

In this experiment, slightly faster decay helped more than slower decay. That does not mean exploration is unimportant. It means the baseline task and network were already simple enough that excessive late exploration became a disadvantage.

## Impact of Updating the Target Network Too Often or Too Rarely

The target-network update frequency produced one of the clearest patterns in the experiments.

### Updating too rarely: `TARGET_UPDATE_FREQ = 20`

This was consistently poor:

- mean evaluation reward: `149.57`
- solve rate: `0/3`

The likely reason is that the target network became too stale. If target values are updated too slowly, the agent keeps learning from old estimates that no longer match the current online network well enough.

### Updating more often: `TARGET_UPDATE_FREQ = 5`

This performed very well:

- mean evaluation reward: `203.29`
- solve rate: `3/3`
- solved episodes: `511`, `596`, `498`

This was also the fastest-learning completed setting overall, because it solved in fewer episodes on average than both the baseline and `EPSILON_DECAY = 0.993`.

So in this codebase, more frequent target updates helped. They were frequent enough to keep training responsive, but not so frequent that learning became obviously unstable.

## Which Hyperparameter Mattered Most

Among the fully completed experiment groups, `TARGET_UPDATE_FREQ` appeared to matter the most.

Why:

- `5` gave strong performance and fast solving
- `20` failed on all three seeds
- the gap between those two settings was very large in both solve rate and final evaluation reward

This suggests that target-network freshness was a major factor for training quality in this implementation.

`EPSILON_DECAY` also mattered a lot, especially because `0.993` and `0.997` produced very different outcomes. But the target-update experiment showed the sharpest practical difference between a good configuration and a bad one.

The learning-rate experiment mattered too, but the currently completed evidence is weaker:

- `2.5e-4` stayed close to baseline performance
- `1e-3` looked poor on the two completed seeded runs, but the third run was still incomplete when this draft was written

## Observed Failure Modes During Training

Several failure modes appeared repeatedly in the weaker configurations.

### 1. Hovering or drifting without finishing the landing

Some agents learned to avoid immediate crashing but still failed to complete the task. This caused long episodes where the lander stayed in the air or moved inefficiently. This behavior is consistent with a partial policy: survival improved, but actual landing control remained weak.

### 2. Excessive exploration

This was most visible with `EPSILON_DECAY = 0.997`. When epsilon stayed high for too long, the agent continued taking too many random actions late in training. That likely prevented it from stabilizing a reliable landing behavior.

### 3. Stale targets

This was most visible with `TARGET_UPDATE_FREQ = 20`. In that setting, the learning signal likely lagged behind the online network too much, which hurt convergence.

### 4. Unstable or overly aggressive updates

The partially completed `LEARNING_RATE = 1e-3` runs were clearly weaker than the baseline so far. A plausible explanation is that updates became too large, making value estimates less stable.

## How the Learned Policy Compares With Intuition About Optimal Landing

The better-performing settings match reasonable intuition about how LunarLander should be solved.

A good landing policy should:

- reduce vertical speed before touchdown
- stay relatively upright
- correct horizontal drift toward the landing pad
- avoid wasting fuel on unnecessary thrust
- make small stabilizing corrections instead of chaotic large movements

The stronger settings, especially `EPSILON_DECAY = 0.993` and `TARGET_UPDATE_FREQ = 5`, are consistent with that intuition because they achieved both higher evaluation rewards and higher solve rates. That suggests the agent learned more stable and deliberate control rather than only surviving longer.

By contrast, the weaker settings appear to have produced policies that were either:

- too random for too long
- too slow to update toward better targets
- or too unstable in their value updates

These failure modes are also consistent with poor landing behavior: drifting, delayed correction, overcorrection, or failing to settle into a soft landing.

## Interpretation of the Baseline

The baseline remained strong throughout the experiments:

- mean evaluation reward: `198.48`
- solve rate: `2/3`

This is a good result, not a disappointing one. It suggests the original default configuration was already a reasonable tradeoff between:

- exploration
- learning speed
- stability

At the same time, the experiments still found better settings:

- `EPSILON_DECAY = 0.993`
- `TARGET_UPDATE_FREQ = 5`

So the conclusion is not that tuning was useless. The conclusion is that the baseline was already good, and only some changes improved on it.

## Main Conclusion

The hyperparameter experiments show that the Vanilla DQN agent is quite sensitive to training configuration.

The best completed results in this report came from:

- `EPSILON_DECAY = 0.993`
- `TARGET_UPDATE_FREQ = 5`

Both outperformed the seeded baseline on average and solved all three seeds. Among them, `TARGET_UPDATE_FREQ = 5` gave the fastest solving behavior, while `EPSILON_DECAY = 0.993` gave the highest mean evaluation reward in the completed seeded runs.

The weakest completed setting was:

- `TARGET_UPDATE_FREQ = 20`

and `EPSILON_DECAY = 0.997` was also clearly poor. These results show that too much exploration and too-stale target values can both significantly hurt learning.

Overall, the most important lesson from the experiments is that controlled comparison across fixed seeds gives a much clearer picture than anecdotal single-run results. In this codebase, the most reliable improvements came from moderate changes that kept learning responsive without making the policy too random or the targets too outdated.
