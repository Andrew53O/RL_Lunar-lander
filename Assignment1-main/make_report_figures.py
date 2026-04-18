from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parent
STATS_PATH = ROOT / "stats.md"
OUTPUT_DIR = ROOT / "outputs" / "report_figures"
EPSILON_FIGURE_PATH = OUTPUT_DIR / "epsilon_decay_comparison.png"
EPSILON_CURVE_FIGURE_PATH = OUTPUT_DIR / "epsilon_schedule_curves.png"
TARGET_UPDATE_FIGURE_PATH = OUTPUT_DIR / "target_update_comparison.png"
LEARNING_RATE_FIGURE_PATH = OUTPUT_DIR / "learning_rate_comparison.png"
EPSILON_START = 1.0
EPSILON_END = 0.01
NUM_EPISODES = 650
PAPER_BG = "#ffffff"
PANEL_BG = "#ffffff"
TEXT_COLOR = "#202020"
GRID_COLOR = "#d9d9d9"
TITLE_FONT = "DejaVu Serif"
BODY_FONT = "DejaVu Serif"
COLOR_MAP = {
    "0.993": "#4c78a8",
    "0.995": "#222222",
    "0.997": "#8c8c8c",
}


def apply_figure_style() -> None:
    plt.rcParams.update(
        {
            "figure.facecolor": PAPER_BG,
            "axes.facecolor": PANEL_BG,
            "axes.edgecolor": "#4f564f",
            "axes.linewidth": 0.8,
            "axes.labelcolor": TEXT_COLOR,
            "axes.titlecolor": TEXT_COLOR,
            "xtick.color": TEXT_COLOR,
            "ytick.color": TEXT_COLOR,
            "font.family": BODY_FONT,
            "font.size": 10,
            "axes.titleweight": "normal",
        }
    )


def parse_stats_table(stats_path: Path) -> list[dict[str, str]]:
    lines = stats_path.read_text(encoding="utf-8").splitlines()
    header = None
    rows: list[dict[str, str]] = []

    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        if stripped.startswith("| ---"):
            continue

        columns = [column.strip() for column in stripped.strip("|").split("|")]
        if header is None:
            header = columns
            continue

        if len(columns) != len(header):
            continue

        rows.append(dict(zip(header, columns)))

    return rows


def select_seeded_epsilon_runs(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    selected = []
    valid_eps = {"0.993", "0.995", "0.997"}
    valid_seeds = {"101", "202", "303"}

    for row in rows:
        if row["Algorithm"] != "Vanilla DQN":
            continue
        if row["Seed"] not in valid_seeds:
            continue
        if row["LR"] not in {"5e-4", "0.0005"}:
            continue
        if row["Target Update"] != "10":
            continue
        if row["Epsilon Decay"] not in valid_eps:
            continue
        selected.append(row)

    return selected


def select_seeded_target_runs(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    selected = []
    valid_targets = {"5", "10", "20"}
    valid_seeds = {"101", "202", "303"}

    for row in rows:
        if row["Algorithm"] != "Vanilla DQN":
            continue
        if row["Seed"] not in valid_seeds:
            continue
        if row["LR"] not in {"5e-4", "0.0005"}:
            continue
        if row["Epsilon Decay"] != "0.995":
            continue
        if row["Target Update"] not in valid_targets:
            continue
        selected.append(row)

    return selected


def select_seeded_learning_rate_runs(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    selected = []
    valid_lrs = {"0.00025", "0.0005", "0.001", "2.5e-4", "5e-4", "1e-3"}
    valid_seeds = {"101", "202", "303"}

    for row in rows:
        if row["Algorithm"] != "Vanilla DQN":
            continue
        if row["Seed"] not in valid_seeds:
            continue
        if row["Epsilon Decay"] != "0.995":
            continue
        if row["Target Update"] != "10":
            continue
        if row["LR"] not in valid_lrs:
            continue
        selected.append(row)

    return selected


def build_group_summary(
    rows: list[dict[str, str]],
    key: str,
    group_order: list[str],
) -> dict[str, dict[str, object]]:
    summary: dict[str, dict[str, object]] = {}

    for group_value in group_order:
        group_rows = [row for row in rows if row[key] == group_value]
        rewards = np.array([float(row["Eval Mean Reward"]) for row in group_rows], dtype=float)
        solved_count = sum(row["Solved At"] != "Not solved" for row in group_rows)
        summary[group_value] = {
            "rewards": rewards,
            "mean_reward": float(np.mean(rewards)),
            "std_reward": float(np.std(rewards)),
            "solve_rate": solved_count / len(group_rows),
            "count": len(group_rows),
        }

    return summary


def make_comparison_figure(
    summary: dict[str, dict[str, object]],
    group_order: list[str],
    y_tick_labels: list[str],
    title: str,
    x_label: str,
    figure_note: str,
    out_path: Path,
    group_color_map: dict[str, str],
) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    apply_figure_style()

    means = [summary[group]["mean_reward"] for group in group_order]
    stds = [summary[group]["std_reward"] for group in group_order]
    solve_rates = [summary[group]["solve_rate"] for group in group_order]
    y_positions = np.arange(len(group_order) - 1, -1, -1, dtype=float)

    fig, ax = plt.subplots(figsize=(7.6, 4.8))

    min_reward = min(float(np.min(summary[group]["rewards"])) for group in group_order)
    max_reward = max(float(np.max(summary[group]["rewards"])) for group in group_order)
    x_min = max(0, min_reward - 18)
    x_max = max_reward + 28

    ax.axvline(
        200,
        color="#6b6b6b",
        linestyle="--",
        linewidth=1.0,
        zorder=1,
    )

    for idx, group in enumerate(group_order):
        color = group_color_map[group]
        rewards = summary[group]["rewards"]
        jitter = np.linspace(-0.09, 0.09, len(rewards))
        y = np.full(len(rewards), y_positions[idx]) + jitter

        ax.scatter(
            rewards,
            y,
            s=40,
            facecolors="white",
            edgecolors=color,
            linewidths=1.0,
            zorder=3,
        )
        ax.hlines(
            y_positions[idx],
            means[idx] - stds[idx],
            means[idx] + stds[idx],
            color=color,
            linewidth=2.0,
            alpha=1.0,
            zorder=2,
            capstyle="round",
        )
        ax.scatter(
            means[idx],
            y_positions[idx],
            s=64,
            color=color,
            edgecolors=color,
            linewidths=0.5,
            zorder=4,
        )

        solve_text = f"{int(round(solve_rates[idx] * 3))}/3 solved"
        ax.text(
            x_max - 0.5,
            y_positions[idx] + 0.20,
            solve_text,
            ha="right",
            va="bottom",
            fontsize=8.5,
            color=TEXT_COLOR,
        )
        ax.text(
            means[idx],
            y_positions[idx] - 0.24,
            f"{means[idx]:.1f}",
            ha="center",
            va="top",
            fontsize=8.5,
            color=TEXT_COLOR,
        )

    ax.text(200, y_positions[0] + 0.44, "target = 200", ha="left", va="bottom", fontsize=8.5, color="#5c5c5c")

    ax.set_yticks(y_positions, y_tick_labels)
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(-0.6, y_positions[0] + 0.6)
    ax.set_xlabel(x_label)
    ax.set_title(title, pad=14, fontfamily=TITLE_FONT, fontsize=13)
    fig.text(
        0.125,
        0.90,
        figure_note,
        fontsize=8.5,
        color="#555555",
        fontfamily=BODY_FONT,
    )
    ax.grid(axis="x", linestyle=":", linewidth=0.7, color=GRID_COLOR, alpha=0.9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#666666")
    ax.spines["bottom"].set_color("#666666")
    fig.tight_layout(rect=[0, 0, 1, 0.9])
    fig.savefig(out_path, dpi=260, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)


def make_epsilon_decay_figure(summary: dict[str, dict[str, object]], out_path: Path) -> None:
    group_order = ["0.993", "0.995", "0.997"]
    y_tick_labels = ["0.993", "0.995 (baseline)", "0.997"]
    make_comparison_figure(
        summary=summary,
        group_order=group_order,
        y_tick_labels=y_tick_labels,
        title="Effect of Epsilon Decay on Final Performance",
        x_label="Evaluation mean reward",
        figure_note="Vanilla DQN, 650 training episodes, 100-episode evaluation, three fixed seeds",
        out_path=out_path,
        group_color_map=COLOR_MAP,
    )


def make_target_update_figure(summary: dict[str, dict[str, object]], out_path: Path) -> None:
    target_color_map = {
        "5": "#4c78a8",
        "10": "#222222",
        "20": "#8c8c8c",
    }
    group_order = ["5", "10", "20"]
    y_tick_labels = ["5", "10 (baseline)", "20"]
    make_comparison_figure(
        summary=summary,
        group_order=group_order,
        y_tick_labels=y_tick_labels,
        title="Effect of Target Update Frequency on Final Performance",
        x_label="Evaluation mean reward",
        figure_note="Vanilla DQN, epsilon decay = 0.995, learning rate = 5e-4, three fixed seeds",
        out_path=out_path,
        group_color_map=target_color_map,
    )


def make_learning_rate_figure(summary: dict[str, dict[str, object]], out_path: Path) -> None:
    lr_color_map = {
        "0.00025": "#4c78a8",
        "0.0005": "#222222",
        "0.001": "#8c8c8c",
    }
    group_order = ["0.00025", "0.0005", "0.001"]
    y_tick_labels = ["0.00025", "0.0005 (baseline)", "0.001"]
    make_comparison_figure(
        summary=summary,
        group_order=group_order,
        y_tick_labels=y_tick_labels,
        title="Effect of Learning Rate on Final Performance",
        x_label="Evaluation mean reward",
        figure_note="Vanilla DQN, epsilon decay = 0.995, target update = 10, three fixed seeds",
        out_path=out_path,
        group_color_map=lr_color_map,
    )


def make_epsilon_schedule_figure(out_path: Path) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    apply_figure_style()

    fig, ax = plt.subplots(figsize=(7.6, 4.8))
    episode_indices = np.arange(1, NUM_EPISODES + 1)
    schedule_specs = [
        ("0.993", COLOR_MAP["0.993"]),
        ("0.995 (baseline)", COLOR_MAP["0.995"]),
        ("0.997", COLOR_MAP["0.997"]),
    ]

    for label, color in schedule_specs:
        decay = float(label.split()[0])
        epsilons = np.maximum(EPSILON_END, EPSILON_START * (decay ** episode_indices))
        ax.plot(
            episode_indices,
            epsilons,
            label=label,
            color=color,
            linewidth=1.8,
        )

    ax.axhline(
        EPSILON_END,
        color="#5c5c5c",
        linestyle="--",
        linewidth=0.9,
        label="Epsilon floor",
    )
    ax.set_title("Exploration Probability Schedule by Epsilon Decay", pad=12, fontfamily=TITLE_FONT, fontsize=13)
    ax.set_xlabel("Episode")
    ax.set_ylabel("Epsilon (exploration probability)")
    ax.set_xlim(1, NUM_EPISODES)
    ax.set_ylim(0, 1.05)
    ax.grid(True, linestyle=":", linewidth=0.7, color=GRID_COLOR, alpha=0.9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    legend = ax.legend(loc="upper right", frameon=True)
    legend.get_frame().set_facecolor("white")
    legend.get_frame().set_edgecolor("#bdbdbd")
    fig.tight_layout()
    fig.savefig(out_path, dpi=260, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)


def main() -> None:
    rows = parse_stats_table(STATS_PATH)
    epsilon_rows = select_seeded_epsilon_runs(rows)
    epsilon_summary = build_group_summary(epsilon_rows, key="Epsilon Decay", group_order=["0.993", "0.995", "0.997"])
    target_rows = select_seeded_target_runs(rows)
    target_summary = build_group_summary(target_rows, key="Target Update", group_order=["5", "10", "20"])
    lr_rows = select_seeded_learning_rate_runs(rows)
    lr_summary = build_group_summary(lr_rows, key="LR", group_order=["0.00025", "0.0005", "0.001"])

    make_epsilon_decay_figure(epsilon_summary, EPSILON_FIGURE_PATH)
    make_epsilon_schedule_figure(EPSILON_CURVE_FIGURE_PATH)
    make_target_update_figure(target_summary, TARGET_UPDATE_FIGURE_PATH)
    make_learning_rate_figure(lr_summary, LEARNING_RATE_FIGURE_PATH)
    print(f"Saved: {EPSILON_FIGURE_PATH}")
    print(f"Saved: {EPSILON_CURVE_FIGURE_PATH}")
    print(f"Saved: {TARGET_UPDATE_FIGURE_PATH}")
    print(f"Saved: {LEARNING_RATE_FIGURE_PATH}")


if __name__ == "__main__":
    main()
