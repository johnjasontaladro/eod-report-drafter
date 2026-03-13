# 📝 EOD Report Drafter

An automated skill for drafting, storing, and consolidating End-of-Day (EOD) reports. Works with Claude AI and GitHub Copilot inside VS Code, managing your daily progress reports locally across chat sessions.

---

## 🚀 How it Works

- **Default behavior:** Invoke `/eod-report-drafter` with no context and the assistant reads your current AI session to draft a report automatically — no input required.
- **Optional context:** You can provide additional details (JIRA tickets, notes, project names) to supplement or focus the report.
- **Automation:** The assistant drafts the report and runs `eod_manager.py` to save it.
- **Organization:** Reports are saved to `~/.claude/skills/eod-report-drafter/reports/<yyyy-mm-dd>/`.
- **Consolidation:** At the end of the day, the assistant retrieves all saved snippets and generates a single, polished report for management.

---

## 🛠️ Installation

This skill works with **Claude Code** (via `~/.claude/skills/`) and **GitHub Copilot in VS Code** (synced via the Compound plugin). Steps 1 and 2 are required for all users. Step 3 is only needed if you use GitHub Copilot in VS Code.

### 1. Clone into the Claude skills directory

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/johnjasontaladro/eod-report-drafter.git ~/.claude/skills/eod-report-drafter
```

This makes the skill available to Claude Code immediately — no further Claude-specific setup needed.

### 2. Make the script executable

```bash
chmod +x ~/.claude/skills/eod-report-drafter/eod_manager.py
```

### 3. Sync to GitHub Copilot (VS Code)

If you use GitHub Copilot in VS Code, sync the skill using the [`compound-plugin` CLI](https://github.com/EveryInc/compound-engineering-plugin):

```bash
bunx @every-env/compound-plugin sync --target copilot
```

This reads all skills in `~/.claude/skills/` and converts them to Copilot-compatible prompts under `~/.copilot/skills/`. After syncing, the `/eod-report-drafter` command becomes available in GitHub Copilot Chat.

> **Prerequisites:** [Bun](https://bun.sh) must be installed. Re-run this command any time you update the skill.

---

## 🔄 Updating

Pull the latest changes:

```bash
cd ~/.claude/skills/eod-report-drafter
git pull
```

If you use GitHub Copilot in VS Code, re-sync:

```bash
bunx @every-env/compound-plugin sync --target copilot
```

If `eod_manager.py` changed, run the test suite to confirm everything still works:

```bash
python3 test_eod_manager.py
```

---

## 📖 Usage

### Individual Task Reports

**No context — reads the current session:**

> "/eod-report-drafter"

The assistant reads your current AI session and drafts a report from whatever you've been working on.

**With a project name:**

> "/eod-report-drafter Project: Nexus"

Scopes the report to a specific project without requiring you to describe the work.

**With notes or a task description:**

> "/eod-report-drafter I refactored the auth middleware to use JWT refresh tokens."

Uses your description directly as the basis for the report.

**With a JIRA ticket and full context:**

> "/eod-report-drafter JIRA-101. Project: Nexus. I finished the API integration and added retry logic."

The assistant uses all provided details to produce a detailed, ticket-linked report.

**With Jira MCP — auto-reads the ticket title:**

If the AI has access to a Jira MCP server, passing just a ticket number works differently from the plain JIRA ticket example above — the assistant actively fetches the ticket title and description from Jira rather than relying on what you type:

> "/eod-report-drafter JIRA-101"

The assistant fetches the ticket title directly from Jira and uses it to produce an accurate, well-named report — no need to describe the work yourself.

**With Jira MCP — pulls in your ticket comment:**

> "/eod-report-drafter JIRA-101. Use my latest comment on the ticket."

The assistant reads your most recent comment on the ticket and uses it as the basis for the report, so any progress note you already wrote in Jira becomes your EOD entry automatically.

**With today's git commits:**

> "/eod-report-drafter Include my commits from today."

The assistant runs `git log` to fetch commits made today, then drafts a report from the commit messages — useful for capturing work done outside of the current AI session.

In every case, the assistant drafts the report and runs the save command automatically.

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

## ⚖️ License

MIT
