# Part D Guide

## Goal

Part D is about **experimentation and explanation**.

By this stage:

- Part A gave you the random baseline
- Part B built the DQN agent
- Part C trained and evaluated one working model

Part D asks you to go one step further:

- change important hyperparameters
- compare the results in a controlled way
- explain what changed and why

This is the part where you show scientific thinking, not just implementation.

## What You Need To Deliver

By the end of Part D, you should have:

- at least `3` hyperparameter variations
- comparison plots or tables
- notes on what improved or got worse
- a short report of about `2` to `3` pages

## Big Idea Of Part D

Part D is not about trying random settings until one works.

It is about asking questions like:

- What happens if epsilon decays faster or slower?
- What happens if the batch size changes?
- What happens if the target network updates too often or too rarely?
- Which hyperparameter has the biggest effect?

You are trying to understand the behavior of your learning system.

## Step 1: Choose Controlled Experiments

The assignment asks for at least `3` hyperparameter variations.

That means you should compare runs in a controlled way.

### Good rule

Change **one important thing at a time**.

Why:

- then you can explain which change caused the result
- the comparison becomes fairer and easier to interpret

### Bad experiment design

Do not change many things at once, such as:

- learning rate
- batch size
- epsilon decay
- target update frequency

all in the same run

If you do that, you will not know what actually caused the improvement or failure.

## Step 2: Good Hyperparameters To Test

Suggested hyperparameters from the assignment:

- learning rate
- batch size
- epsilon decay
- network size
- target update frequency
- replay buffer size

For a first clean Part D, the easiest strong choices are:

- epsilon decay
- learning rate
- batch size

These are easier to explain clearly in the report.

## Step 3: Suggested Experiment Sets

Here are good beginner-friendly experiment groups.

### Option A: Epsilon decay

Compare:

- slower decay
- default decay
- faster decay

Question to answer:

- Does more exploration help learning more, or does it slow down final performance?

### Option B: Learning rate

Compare:

- smaller learning rate
- default learning rate
- larger learning rate

Question to answer:

- Does the network learn more stably with a smaller learning rate?
- Does a larger learning rate make training unstable?

### Option C: Batch size

Compare:

- smaller batch size
- default batch size
- larger batch size

Question to answer:

- Does a larger batch produce smoother learning?
- Does a smaller batch make learning noisier?

### Option D: Target update frequency

Compare:

- more frequent updates
- default update frequency
- less frequent updates

Question to answer:

- Does updating too often make the target unstable?
- Does updating too rarely make learning too slow?

## Step 4: Keep A Baseline Configuration

Before experiments, define one default setting as your baseline.

Example idea:

```text
learning_rate = 5e-4
batch_size = 64
epsilon_decay = 0.995
target_update_freq = 10
buffer_size = 10000
```

This baseline run gives you the reference point.

Every experiment should be compared against this baseline.

## Step 5: What To Record For Every Run

For each experiment run, record:

- algorithm name
- hyperparameter changed
- exact value used
- number of training episodes
- training time
- device used (`cpu` or `cuda`)
- final evaluation mean reward
- whether the solved threshold was reached
- `solved_at` if applicable

Your `stats.md` file is a good place to store this run-by-run information.

## Step 6: What To Compare Across Runs

For each variation, compare:

- final evaluation mean reward
- success rate
- training curve shape
- learning speed
- stability
- whether the run solved the environment

### Learning speed

Ask:

- Which setting improves reward faster?
- Which setting reaches strong performance earlier?

### Final performance

Ask:

- Which setting finishes with the best evaluation reward?
- Which setting has the best success rate?

### Stability

Ask:

- Which setting has smoother reward curves?
- Which setting avoids very unstable loss or Q-value behavior?

## Step 7: What A Good Comparison Looks Like

A good comparison says something like:

> When epsilon decayed too quickly, the agent explored less and reached a weaker final policy. When epsilon decayed more slowly, learning started more slowly but final performance was better.

This is much better than saying:

> Setting B was better than setting A.

Because in Part D, explanation matters as much as numbers.

## Step 8: Use Plots To Support Claims

Good experiment evidence includes:

- reward curves for each run
- evaluation summary table
- run statistics from `stats.md`

If you compare three settings, try to show:

- one plot with three reward curves, or
- separate saved plots with a clear summary table

The main point is:

- your claims in the report should match the plots

## Step 9: Questions You Should Be Able To Answer

Your report should be able to answer questions like:

- How did epsilon decay affect learning speed and final performance?
- What happened when the target network updated too often or too rarely?
- Which hyperparameter had the strongest effect?
- What failure modes appeared during training?
- How does the learned policy compare with intuition about good landing behavior?

These are not just writing prompts.
They are the core ideas Part D wants you to understand.

## Step 10: Common Failure Modes To Watch For

When doing experiments, look for:

- reward staying flat and negative
- reward improving and then collapsing
- loss becoming `nan`
- Q-values becoming unrealistically large
- the agent learning unstable spinning behavior
- the agent hovering or wasting fuel instead of landing
- the agent improving during training but performing badly in evaluation

These failure modes are valuable report material.

If something fails, that does not mean the run is useless.
It means you discovered something important about the hyperparameter choice.

## Step 11: How To Write The Report

Your report should be short, but thoughtful.

A good structure is:

1. Brief setup
2. Baseline configuration
3. Experiment choices
4. Results
5. Interpretation
6. Conclusion

### 1. Brief setup

Describe:

- environment
- algorithm used
- general training setup

### 2. Baseline configuration

State the default hyperparameters clearly.

### 3. Experiment choices

List what you changed and why.

Example:

- tested three epsilon decay values to study exploration speed vs final performance

### 4. Results

Show:

- plots
- tables
- run summaries

### 5. Interpretation

Explain:

- what changed
- what the curves show
- what the videos suggest
- why you think the result happened

### 6. Conclusion

Summarize:

- which setting worked best
- which setting was most stable
- what you learned

## Step 12: Helpful Writing Style For Part D

Try to write in this style:

- clear
- specific
- evidence-based

Good example:

> Increasing the batch size made the reward curve smoother, but it did not improve final performance much. The medium batch size gave the best balance between stability and final reward.

Less useful example:

> The result was better.

Always try to connect:

- hyperparameter change
- effect on training
- effect on final performance
- possible reason

## Step 13: Suggested Workflow For Part D

1. Choose one baseline configuration.
2. Choose one hyperparameter family to test first.
3. Run at least three controlled variants.
4. Save results and note the run settings in `stats.md`.
5. Compare plots and final evaluation statistics.
6. Write down observations immediately in `REPORT.md`.
7. Repeat for another hyperparameter if needed.
8. Write the final report.

## Common Mistakes In Part D

- changing too many hyperparameters at once
- not keeping a baseline
- only comparing one final number
- ignoring training instability
- making claims without plots
- choosing settings but not recording what changed
- forgetting to discuss failure cases

## Definition Of Done

Part D is done when all of these are true:

- [ ] at least `3` hyperparameter variations were tested
- [ ] each run has a clearly recorded configuration
- [ ] the runs are compared fairly against a baseline
- [ ] comparison plots or summary tables are available
- [ ] the main effects of the hyperparameters are explained
- [ ] failure modes are discussed if they occurred
- [ ] the final report is written clearly and supported by evidence

## Final Reminder

Part D is not about finding the single highest score only.

It is about being able to say:

- what you changed
- what happened
- why it likely happened
- which setting you would choose and why

That is what makes the assignment look complete and thoughtful.
