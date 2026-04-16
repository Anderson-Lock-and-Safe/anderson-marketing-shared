# Anderson Marketing Shared

Shared resources for all Anderson Lock & Safe marketing agents.

## What's Here

| Directory | Contents |
|-----------|----------|
| `tools/` | Python scripts — Buffer publishing, Gemini video analysis, Google Chat |
| `workflows/` | SOPs for all marketing operations |
| `workflows/tasks/` | Step-by-step task workflows |
| `workflows/templates/` | Brief and report templates |

## Shared Docs

| File | Purpose |
|------|---------|
| `WAT_framework.md` | Core agent operating principles |
| `anderson-lock-and-safe-ai-guidelines.md` | Brand voice, values, audience |
| `engagement-posts-calendar-apr-may-2026.md` | Active social content calendar |
| `agent-architecture.md` | Three-tier Planner/Creator/Executor pattern |
| `task-reporting-protocol.md` | How agents report on completed tasks |
| `handoff-protocol.md` | How agents pass work to other agents |

## Used By

Each agent repo clones this shared repo at `/tmp/shared` during setup.
Agent-specific subagents and prompts live in their own repos.
