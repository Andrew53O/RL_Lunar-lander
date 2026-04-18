import argparse
from dataclasses import dataclass
import multiprocessing as mp
from pathlib import Path
import re
import shlex
import subprocess
import time


COMPLETE_MARKERS = {"[c]", "[x]", "[done]"}


@dataclass
class CommandJob:
    run_name: str
    command: str
    completed: bool


def parse_table_statuses(markdown_text: str) -> dict[str, bool]:
    statuses: dict[str, bool] = {}

    for line in markdown_text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        if "Run Name" in stripped or "---" in stripped:
            continue

        columns = [column.strip() for column in stripped.strip("|").split("|")]
        if len(columns) < 2:
            continue

        run_name = columns[0].strip("`")
        status_text = columns[1].lower()
        statuses[run_name] = status_text in COMPLETE_MARKERS

    return statuses


def parse_command_blocks(markdown_text: str) -> list[tuple[str, str]]:
    commands: list[tuple[str, str]] = []
    lines = markdown_text.splitlines()
    index = 0

    while index < len(lines):
        line = lines[index].strip()
        heading_match = re.match(r"##\s+`([^`]+)`", line)
        if not heading_match:
            index += 1
            continue

        run_name = heading_match.group(1)
        index += 1

        while index < len(lines) and not lines[index].strip():
            index += 1

        if index >= len(lines) or lines[index].strip() != "```bash":
            raise ValueError(f"Expected a bash code block after heading for {run_name}.")

        index += 1
        command_lines: list[str] = []

        while index < len(lines) and lines[index].strip() != "```":
            if lines[index].strip():
                command_lines.append(lines[index].strip())
            index += 1

        if index >= len(lines):
            raise ValueError(f"Unclosed code block for {run_name}.")

        command = " ".join(command_lines).strip()
        if not command:
            raise ValueError(f"Empty command block for {run_name}.")

        commands.append((run_name, command))
        index += 1

    return commands


def load_jobs(commands_path: Path) -> list[CommandJob]:
    markdown_text = commands_path.read_text(encoding="utf-8")
    statuses = parse_table_statuses(markdown_text)
    commands = parse_command_blocks(markdown_text)

    jobs: list[CommandJob] = []
    for run_name, command in commands:
        jobs.append(
            CommandJob(
                run_name=run_name,
                command=command,
                completed=statuses.get(run_name, False),
            )
        )

    return jobs


def execute_job(payload: tuple[str, str, str, str]) -> dict:
    run_name, command, workdir, logs_dir = payload
    log_path = Path(logs_dir) / f"{run_name}.log"
    started_at = time.perf_counter()

    with log_path.open("w", encoding="utf-8") as log_file:
        log_file.write(f"Run name: {run_name}\n")
        log_file.write(f"Command : {command}\n\n")
        log_file.flush()

        process = subprocess.run(
            shlex.split(command),
            cwd=workdir,
            stdout=log_file,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )

    elapsed_seconds = time.perf_counter() - started_at
    return {
        "run_name": run_name,
        "command": command,
        "returncode": process.returncode,
        "elapsed_seconds": elapsed_seconds,
        "log_path": str(log_path),
    }


def mark_completed(commands_path: Path, successful_run_names: set[str]) -> None:
    lines = commands_path.read_text(encoding="utf-8").splitlines()
    updated_lines: list[str] = []

    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("|") or "Run Name" in stripped or "---" in stripped:
            updated_lines.append(line)
            continue

        columns = [column.strip() for column in stripped.strip("|").split("|")]
        if len(columns) < 2:
            updated_lines.append(line)
            continue

        run_name = columns[0].strip("`")
        if run_name in successful_run_names:
            columns[1] = "[c]"
            updated_lines.append("| " + " | ".join(columns) + " |")
        else:
            updated_lines.append(line)

    commands_path.write_text("\n".join(updated_lines) + "\n", encoding="utf-8")


def format_duration(seconds: float) -> str:
    total_seconds = int(round(seconds))
    minutes = total_seconds // 60
    secs = total_seconds % 60
    return f"{minutes:02d}:{secs:02d}"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run multiple experiment commands from COMMANDS.md in parallel."
    )
    parser.add_argument(
        "--commands-file",
        type=str,
        default="COMMANDS.md",
        help="Markdown file that contains the run checklist and command blocks.",
    )
    parser.add_argument(
        "--max-workers",
        type=int,
        default=2,
        help="Maximum number of experiment processes to run at the same time.",
    )
    parser.add_argument(
        "--include-completed",
        action="store_true",
        help="Include commands already marked as completed in COMMANDS.md.",
    )
    parser.add_argument(
        "--run-names",
        nargs="*",
        default=None,
        help="Optional list of specific run names to execute.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print which commands would run without starting them.",
    )
    args = parser.parse_args()

    if args.max_workers < 1:
        raise ValueError("--max-workers must be at least 1.")

    script_dir = Path(__file__).resolve().parent
    commands_path = Path(args.commands_file)
    if not commands_path.is_absolute():
        commands_path = script_dir / commands_path

    jobs = load_jobs(commands_path)

    if not args.include_completed:
        jobs = [job for job in jobs if not job.completed]

    if args.run_names:
        selected_run_names = set(args.run_names)
        jobs = [job for job in jobs if job.run_name in selected_run_names]

    if not jobs:
        print("No commands matched the current filters.")
        return

    print(f"Loaded {len(jobs)} command(s) from {commands_path.name}.")
    for job in jobs:
        print(f"- {job.run_name}: {job.command}")

    if args.dry_run:
        print("\nDry run only. No commands were started.")
        return

    logs_dir = script_dir / "outputs" / "launcher_logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    worker_count = min(args.max_workers, len(jobs))
    print(f"\nStarting {len(jobs)} job(s) with max_workers={worker_count}.")
    print(f"Per-run logs will be written to: {logs_dir}")

    payloads = [
        (job.run_name, job.command, str(script_dir), str(logs_dir))
        for job in jobs
    ]

    successful_run_names: set[str] = set()
    failed_runs: list[dict] = []

    ctx = mp.get_context("spawn")
    with ctx.Pool(processes=worker_count) as pool:
        for result in pool.imap_unordered(execute_job, payloads):
            status = "OK" if result["returncode"] == 0 else "FAIL"
            print(
                f"[{status}] {result['run_name']} finished in "
                f"{format_duration(result['elapsed_seconds'])} "
                f"(log: {result['log_path']})"
            )

            if result["returncode"] == 0:
                successful_run_names.add(result["run_name"])
            else:
                failed_runs.append(result)

    if successful_run_names:
        mark_completed(commands_path, successful_run_names)
        print(f"\nMarked {len(successful_run_names)} run(s) as completed in {commands_path.name}.")

    if failed_runs:
        print("\nSome runs failed:")
        for result in failed_runs:
            print(f"- {result['run_name']} (exit code {result['returncode']}): {result['log_path']}")
    else:
        print("\nAll launched runs completed successfully.")


if __name__ == "__main__":
    main()
