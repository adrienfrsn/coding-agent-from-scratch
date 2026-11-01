import json, shutil, subprocess, sys, tempfile, time
from pathlib import Path

ROOT = Path(__file__).parent
AGENT = ROOT / "agent.py"
RUNS = 3  # l'agent n'est pas déterministe, chaque tâche est jouée plusieurs fois


def run_task(task_dir: Path) -> tuple[bool, float]:
    config = json.loads((task_dir / "task.json").read_text())
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp) / "repo"
        shutil.copytree(task_dir / "repo", work)  # copie propre à chaque essai

        debut = time.time()
        try:
            subprocess.run(
                [sys.executable, str(AGENT), "--task", config["prompt"], "--yes"],
                cwd=work, timeout=600, capture_output=True, text=True,
            )
        except subprocess.TimeoutExpired:
            pass
        duree = time.time() - debut

        for f in config.get("protected", []):
            shutil.copy(task_dir / "repo" / f, work / f)
        verdict = subprocess.run(config["check"], shell=True, cwd=work, capture_output=True)
        return verdict.returncode == 0, duree


if __name__ == "__main__":
    total = reussis = 0
    for task_dir in sorted((ROOT / "tasks").iterdir()):
        for i in range(RUNS):
            ok, duree = run_task(task_dir)
            total += 1
            reussis += ok
            print(f"{'✅' if ok else '❌'} {task_dir.name} #{i + 1} ({duree:.0f} s)")
    print(f"\nTaux de réussite : {reussis}/{total} ({100 * reussis / total:.0f} %)")
