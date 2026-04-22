# Anderson Marketing Shared

Cross-agent context for all Anderson Lock & Safe marketing agents (Social Media Manager, PPC Specialist, Email Marketing, Lead Gen, Content Strategist).

Everything in this repo is read by every agent. Agent-specific workflows, subagents, and tools live in their own agent repos.

## Contents

| File | Purpose |
|------|---------|
| `WAT_framework.md` | Core agent operating principles (Workflows / Agents / Tools) |
| `agent-architecture.md` | Three-tier Planner / Creator / Executor pattern |
| `anderson-lock-and-safe-ai-guidelines.md` | Brand voice, values, audience, tone |
| `brand/style_guide.md` | Design tokens (colors, fonts, layout) |
| `brand/style_references.md` | Visual reference patterns + common-pattern checklist |
| `handoff-protocol.md` | How agents pass work to other agents |
| `task-reporting-protocol.md` | How agents report on completed tasks |

## Used By

Each agent routine clones this repo at `/tmp/shared` during setup. Agent-specific assets live in separate repos:

- `social-media-manager-agent` — subagents + SM workflows
- `ppc-specialist-agent` — subagents + PPC workflows
- `email-marketing-agent` — subagents + email workflows
- `leadgen-agent` — subagents + lead gen workflows
- `content-strategist-agent` — subagents + content strategy workflows

## What Does NOT Belong Here

- Agent-specific workflows (live in the agent repo)
- Agent-specific subagent prompts (live in the agent repo's `.claude/agents/`)
- Agent-specific Python tools (live in the agent repo's `tools/` or be replaced by MCP calls)
- Time-sensitive calendars / campaign state (live in ClickUp / Buffer / Klaviyo — never duplicate)
- API keys or environment variables
