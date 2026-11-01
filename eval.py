import json, shutil, subprocess, sys, tempfile, time
from pathlib import Path

ROOT = Path(__file__).parent
AGENT = ROOT / "agent.py"
RUNS = 3  # the agent is not deterministic, each task is run several times


def run_task(task_dir: Path) -> tuple[bool, float]:
    config = json.loads((task_dir / "task.json").read_text())
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp) / "repo"
        shutil.copytree(task_dir / "repo", work)  # clean copy for each attempt

        start = time.time()
        try:
            subprocess.run(
                [sys.executable, str(AGENT), "--task", config["prompt"], "--yes"],
                cwd=work, timeout=600, capture_output=True, text=True,
            )
        except subprocess.TimeoutExpired:
            pass
        duration = time.time() - start

        for f in config.get("protected", []):
            shutil.copy(task_dir / "repo" / f, work / f)
        verdict = subprocess.run(config["check"], shell=True, cwd=work, capture_output=True)
        return verdict.returncode == 0, duration


if __name__ == "__main__":
    total = passed = 0
    for task_dir in sorted((ROOT / "tasks").iterdir()):
        for i in range(RUNS):
            ok, duration = run_task(task_dir)
            total += 1
            passed += ok
            print(f"{'✅' if ok else '❌'} {task_dir.name} #{i + 1} ({duration:.0f} s)")
    print(f"\nSuccess rate: {passed}/{total} ({100 * passed / total:.0f}%)")
