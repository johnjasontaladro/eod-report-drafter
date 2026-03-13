import os
import re
import stat
import argparse
from datetime import datetime
from pathlib import Path

# Explicitly set the report directory relative to your home folder
BASE_DIR = Path.home() / ".claude/skills/eod-report-drafter/reports"

MAX_CONTENT_BYTES = 100 * 1024 * 1024  # 100 MB

PROJECT_NAME_RE = re.compile(r'^[a-zA-Z0-9_-]+$')


def validate_project_name(project: str) -> None:
    """Reject project names that contain path traversal or glob characters."""
    if not PROJECT_NAME_RE.match(project):
        raise SystemExit(
            f"ERROR: Invalid project name '{project}'. "
            "Only letters, numbers, hyphens, and underscores are allowed."
        )


def assert_within_base_dir(path: Path) -> None:
    """Hard backstop: raise if resolved path escapes BASE_DIR."""
    resolved = path.resolve()
    base_resolved = BASE_DIR.resolve()
    if not str(resolved).startswith(str(base_resolved) + os.sep):
        raise SystemExit(
            f"ERROR: Resolved path '{resolved}' is outside the reports directory."
        )


def get_today_dir():
    today = datetime.now().strftime("%Y-%m-%d")
    path = BASE_DIR / today
    path.mkdir(parents=True, exist_ok=True)
    return path

def save_report(project, content):
    validate_project_name(project)

    if len(content.encode()) > MAX_CONTENT_BYTES:
        raise SystemExit("ERROR: Content exceeds the 100 MB maximum allowed size.")

    target_dir = get_today_dir()

    # Logic: eod-report-PROJECT_NAME-RUNNING_NUMBER.md
    existing_files = list(target_dir.glob(f"eod-report-{project}-*.md"))
    next_num = len(existing_files) + 1

    filename = f"eod-report-{project}-{next_num:02d}.md"
    file_path = target_dir / filename

    assert_within_base_dir(file_path)

    with open(file_path, "w") as f:
        f.write(content.strip())

    os.chmod(file_path, stat.S_IRUSR | stat.S_IWUSR)  # 0o600 — owner read/write only
    return file_path

def consolidate():
    target_dir = get_today_dir()
    files = sorted(list(target_dir.glob("*.md")))
    if not files:
        return "No reports found for today."
    
    combined = []
    for f in files:
        with open(f, 'r') as file:
            combined.append(f"### Source: {f.name}\n{file.read()}\n")
    return "\n".join(combined)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--save", action="store_true")
    parser.add_argument("--consolidate", action="store_true")
    parser.add_argument("--project", type=str)
    parser.add_argument("--content", type=str)
    
    args = parser.parse_args()
    
    if args.save and args.project and args.content:
        path = save_report(args.project, args.content)
        print(f"SUCCESS: Saved to {path}")
    elif args.consolidate:
        print(consolidate())
