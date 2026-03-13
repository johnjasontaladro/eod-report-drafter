import os
import argparse
from datetime import datetime
from pathlib import Path

# Explicitly set the report directory relative to your home folder
BASE_DIR = Path.home() / ".claude/skills/eod-report-drafter/reports"

def get_today_dir():
    today = datetime.now().strftime("%Y-%m-%d")
    path = BASE_DIR / today
    path.mkdir(parents=True, exist_ok=True)
    return path

def save_report(project, content):
    target_dir = get_today_dir()
    
    # Logic: eod-report-PROJECT_NAME-RUNNING_NUMBER.md
    existing_files = list(target_dir.glob(f"eod-report-{project}-*.md"))
    next_num = len(existing_files) + 1
    
    filename = f"eod-report-{project}-{next_num:02d}.md"
    file_path = target_dir / filename
    
    with open(file_path, "w") as f:
        f.write(content.strip())
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
