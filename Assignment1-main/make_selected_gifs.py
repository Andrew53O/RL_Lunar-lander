import io
import os
from contextlib import redirect_stdout
from pathlib import Path
import random
import re
import shutil

import numpy as np
import torch
import torch.nn as nn

from utils import record_episodes


ROOT = Path(__file__).resolve().parent
PART_B_DIR = ROOT / "outputs" / "part_b"
OUT_DIR = ROOT / "outputs" / "report_gifs"
TMP_DIR = OUT_DIR / "_tmp_batches"
DEVICE = torch.device("cpu")
STATE_DIM = 8
ACTION_DIM = 4
HIDDEN_DIM = 128
BATCH_EPISODES = 4
MAX_ATTEMPTS_PER_GROUP = 6

RUN_GROUPS = {
    "good_eps": {
        "run_name": "v_eps993_s202",
        "label": "epsilon_decay_0.993",
    },
    "good_target": {
        "run_name": "v_target5_s101",
        "label": "target_update_5",
    },
    "normal_baseline": {
        "run_name": "v_base_s202",
        "label": "baseline",
    },
    "bad_eps": {
        "run_name": "v_eps997_s101",
        "label": "epsilon_decay_0.997",
    },
    "bad_lr": {
        "run_name": "v_lr1e3_s303",
        "label": "learning_rate_0.001",
    },
}


class QNetwork(nn.Module):
    def __init__(self, state_dim: int, action_dim: int, hidden_dim: int = HIDDEN_DIM):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, action_dim),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


class LoadedPolicy:
    def __init__(self, checkpoint_path: Path):
        self.q_network = QNetwork(STATE_DIM, ACTION_DIM).to(DEVICE)
        checkpoint = torch.load(checkpoint_path, map_location=DEVICE)
        self.q_network.load_state_dict(checkpoint["model_state_dict"])
        self.q_network.eval()

    def act(self, state: np.ndarray) -> int:
        state_tensor = torch.tensor(state, dtype=torch.float32, device=DEVICE).unsqueeze(0)
        with torch.no_grad():
            q_values = self.q_network(state_tensor)
        return int(torch.argmax(q_values, dim=1).item())


def parse_record_output(output_text: str) -> list[dict]:
    results = []
    pattern = re.compile(r"Episode\s+(\d+)\s+reward =\s*([-\d.]+)\s+→\s+(.+)$")

    for line in output_text.splitlines():
        match = pattern.search(line)
        if not match:
            continue
        results.append(
            {
                "episode_index": int(match.group(1)),
                "reward": float(match.group(2)),
                "gif_path": Path(match.group(3).strip()),
            }
        )

    return results


def record_one_episode(policy: LoadedPolicy, out_dir: Path, attempt_seed: int) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)

    random.seed(attempt_seed)
    np.random.seed(attempt_seed)
    torch.manual_seed(attempt_seed)

    stdout_buffer = io.StringIO()
    print(f"  start record_episodes -> {out_dir}")
    with redirect_stdout(stdout_buffer):
        record_episodes(
            num_episodes=1,
            out_dir=str(out_dir),
            policy_fn=policy.act,
        )
    print(f"  finished record_episodes -> {out_dir}")
    results = parse_record_output(stdout_buffer.getvalue())
    if not results:
        raise RuntimeError(f"No episode result was parsed from {out_dir}")
    return results[0]


def collect_episode(run_name: str, mode: str) -> dict:
    checkpoint_path = PART_B_DIR / run_name / "checkpoints" / "dqn_final.pt"
    if not checkpoint_path.exists():
        raise FileNotFoundError(f"Missing checkpoint: {checkpoint_path}")

    policy = LoadedPolicy(checkpoint_path)
    attempts: list[dict] = []

    for attempt in range(1, MAX_ATTEMPTS_PER_GROUP + 1):
        attempt_dir = TMP_DIR / f"{run_name}_attempt{attempt}"
        attempt_seed = 1000 * attempt + len(run_name)
        print(f"Recording attempt {attempt} for {run_name}...")
        result = record_one_episode(policy, attempt_dir, attempt_seed)
        attempts.append(result)
        reward = result["reward"]
        print(f"  reward = {reward:.2f}")

        if mode == "good" and reward >= 200:
            return result
        if mode == "normal" and 140 <= reward <= 205:
            return result
        if mode == "bad" and reward <= 120:
            return result

    if mode == "good":
        return max(attempts, key=lambda item: item["reward"])
    if mode == "normal":
        return min(attempts, key=lambda item: abs(item["reward"] - 180))
    if mode == "bad":
        return min(attempts, key=lambda item: item["reward"])
    raise ValueError(f"Unknown mode: {mode}")


def write_manifest(selections: list[dict]) -> None:
    manifest_path = OUT_DIR / "selection_summary.md"
    with manifest_path.open("w", encoding="utf-8") as f:
        f.write("# Selected Report GIFs\n\n")
        f.write("| Category | Source Run | Reward | GIF |\n")
        f.write("| --- | --- | --- | --- |\n")
        for item in selections:
            f.write(
                f"| {item['category']} | {item['run_name']} | "
                f"{item['reward']:.2f} | {item['filename']} |\n"
            )


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    TMP_DIR.mkdir(parents=True, exist_ok=True)

    selections = []
    plans = [
        ("good_1", "good_eps", "good"),
        ("good_2", "good_target", "good"),
        ("normal_1", "normal_baseline", "normal"),
        ("bad_1", "bad_eps", "bad"),
        ("bad_2", "bad_lr", "bad"),
    ]

    for category, group_key, mode in plans:
        run_name = RUN_GROUPS[group_key]["run_name"]
        label = RUN_GROUPS[group_key]["label"]
        print(f"\nSelecting {category} from {run_name} ({mode})")
        chosen = collect_episode(run_name, mode)
        destination = OUT_DIR / f"{category}_{label}.gif"
        shutil.copy2(chosen["gif_path"], destination)

        selections.append(
            {
                "category": category,
                "run_name": run_name,
                "reward": chosen["reward"],
                "filename": destination.name,
            }
        )
        print(f"{category}: {run_name} -> reward {chosen['reward']:.2f} -> {destination}")

    write_manifest(selections)
    print(f"Saved manifest -> {OUT_DIR / 'selection_summary.md'}")


if __name__ == "__main__":
    main()
