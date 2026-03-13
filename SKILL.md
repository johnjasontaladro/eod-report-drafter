---
name: eod-report-drafter
description: Automated EOD report manager for VS Code. Drafts, saves, and consolidates daily task reports using the local eod_manager.py script.
---

# End of Day Report Drafter

Automate the drafting and storage of daily progress reports directly within VS Code.

## Automation Setup

- **Manager Script:** `python3 ~/.claude/skills/eod-report-drafter/eod_manager.py`
- **Storage Root:** `~/.claude/skills/eod-report-drafter/`

## Modes of Operation

### 1. Draft & Auto-Save Mode

When provided with task details, Jira tickets, or notes:

1. **Draft:** Create a report using the [Output Structure].
2. **Identify Project:** If the project name is missing from the input, ask the user for it (e.g., "Nexus", "Portal").
3. **Execute Save:** Proactively run the following command in a terminal:
   `python3 ~/.claude/skills/eod-report-drafter/eod_manager.py --save --project "PROJECT_NAME" --content "DRAFTED_CONTENT"`
4. **Confirm:** Verify the save was successful and tell the user the filename created.

### 2. Consolidation Mode

When the user wants to "Consolidate," "Finish for the day," or "Generate final report":

1. **Fetch All Snippets:** Run the following command in a terminal:
   `python3 ~/.claude/skills/eod-report-drafter/eod_manager.py --consolidate`
2. **Process Data:** Read the combined output provided by the script.
3. **Draft Final Report:** - Group "What I did today" items by project or ticket.
   - Combine "Next steps" into a single, high-level plan.
   - Use a professional, executive-friendly tone.
4. **Display:** Present only the final, polished report to the user.

## Core Behavior & Tone

- **Voice:** Use first person ("I").
- **Perspective:** Write as if you are the user who performed the work.
- **Level:** High-level. Minimize technical jargon unless the source text specifically demands it.
- **Accuracy:** Do not hallucinate progress. Only report what is supported by the source text.

## Output Structure (Individual Drafts)

Always use this format:

[Month Day, Year]

What I did today:

- [Ticket or task title]
  - [High-level activity 1]
  - [High-level activity 2]

What I will be doing the next working day:

- [Ticket or task title]
  - [Next step 1]
  - [Next step 2]

## Writing Rules

- Use short, clear bullet points.
- Keep Jira Ticket IDs exactly as provided.
- Do not claim work is "finished" or "tested" unless explicitly confirmed by the user.
