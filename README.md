# 📝 EOD Report Drafter

An automated skill for drafting, storing, and consolidating End-of-Day (EOD) reports. Works with Claude AI and GitHub Copilot inside VS Code, managing your daily progress reports locally across chat sessions.

---

## 🚀 How it Works

- **Drafting:** You tell your AI assistant what you worked on.
- **Automation:** The assistant drafts the report and runs `eod_manager.py` to save it.
- **Organization:** Reports are saved to `~/.claude/skills/eod-report-drafter/reports/<yyyy-mm-dd>/`.
- **Consolidation:** At the end of the day, the assistant retrieves all snippets and generates a single, polished report for management.

---

## 🛠️ Installation

### 1. Clone directly into the skills directory

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/johnjasontaladro/eod-report-drafter.git ~/.claude/skills/eod-report-drafter
```

### 2. Make the script executable

```bash
chmod +x ~/.claude/skills/eod-report-drafter/eod_manager.py
```

---

## 🔄 Updating

When changes are pushed to the repo, pull them into your local installation:

```bash
cd ~/.claude/skills/eod-report-drafter
git pull
```

Then re-sync to GitHub Copilot so the updated skill is picked up:

```bash
bunx @every-env/compound-plugin sync --target copilot
```

If the update changed `eod_manager.py`, run the test suite to confirm everything still works:

```bash
python3 test_eod_manager.py
```

---

## 📖 Usage

### Individual Task Reports

Tell your assistant what you've done:

> "Invoke eod-report-drafter for JIRA-101. Project: Nexus. I finished the API integration."

The assistant will draft the report and run the save command automatically.

### Final Consolidation

When you're ready to submit your final report:

> "Consolidate my reports for today."

The assistant reads all saved snippets from today and creates a unified, professional summary.

---

## 📂 File Structure

```plaintext
~/.claude/skills/eod-report-drafter/
├── SKILL.md
├── eod_manager.py
├── test_eod_manager.py
└── reports/
    └── 2026-03-14/
        ├── eod-report-Nexus-01.md
        ├── eod-report-Nexus-02.md
        └── eod-report-Portal-01.md
```

---

## 🧪 Tests

The test suite (`test_eod_manager.py`) covers input validation, path-sandbox enforcement, file permission hardening, and the content-size cap.

### Run tests locally

```bash
cd ~/.claude/skills/eod-report-drafter
python3 test_eod_manager.py
```

Every line should print `PASS`. A non-zero exit code means at least one test failed.

### When to update the tests

When you change `eod_manager.py`, update `test_eod_manager.py` to cover any new behaviour:

1. **New validation rule** (e.g., relaxing the project-name regex) → add a test case that asserts both the new allowed value passes and formerly-allowed values still pass.
2. **New CLI argument** → add tests for its validation and happy-path behaviour.
3. **Changed error message** → update the string assertion in the relevant test case.
4. **New file-system operation** → add a test that writes a fixture, asserts the expected outcome, then cleans it up.

After updating, run the suite locally before pushing. CI will also run it automatically on every push and pull request.

---

## ⚙️ Logic Details

- **Running Numbers:** The script checks the project name and automatically increments the report number (e.g., `-01`, `-02`) to prevent overwriting.
- **Perspective:** All reports are written in the first person ("I").
- **Tone:** High-level and business-friendly, avoiding unnecessary technical jargon unless specified.

---

## 🤖 GitHub Copilot

Sync the skill to GitHub Copilot using the [`compound-plugin` CLI](https://github.com/EveryInc/compound-engineering-plugin):

```bash
bunx @every-env/compound-plugin sync --target copilot
```

This reads all skills installed at `~/.claude/skills/` and converts them to Copilot-compatible prompts, writing them to `~/.copilot/skills/`. After syncing, the `/eod-report-drafter` command becomes available in GitHub Copilot Chat.

> **Prerequisites:** [Bun](https://bun.sh) must be installed. The skill must be installed at `~/.claude/skills/eod-report-drafter/` (see Installation above).

---

## ⚖️ License

MIT
