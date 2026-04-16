# Workflows Index

This directory contains the operational SOPs for Anderson Lock and Safe's AI marketing department, built on the [WAT framework](../WAT_framework.md).

## How It's Organized

Workflows are **layered** — role-level workflows define responsibilities and context, then reference task-level sub-workflows for specific operations.

```
workflows/
├── social-media.md              ← Role: Social Media Manager
├── ppc.md                       ← Role: PPC Specialist
├── email-marketing.md           ← Role: Email Marketing Specialist
├── content-strategy.md          ← Role: Content/SEO Manager (Phase 5)
├── lead-generation.md           ← Role: Lead Gen / Apollo (Phase 6)
│
├── tasks/
│   ├── generate-engagement-post.md    ← Generate a social post from calendar
│   ├── schedule-buffer-posts.md       ← Schedule posts via Buffer MCP
│   ├── review-social-performance.md   ← Analyze social engagement metrics
│   ├── analyze-ppc-performance.md     ← Cross-platform ad performance report
│   ├── optimize-ppc-keywords.md       ← Keyword bids, negatives, search terms
│   ├── audit-klaviyo-flows.md         ← Diagnose email issues, assess flows
│   ├── create-klaviyo-campaign.md     ← Build and schedule email campaigns
│   ├── setup-clickup-campaign.md      ← Create ClickUp structure (Phase 2)
│   ├── generate-content-kit.md        ← Full pillar content kit (Phase 5)
│   ├── monthly-brainstorm-prep.md     ← Pre-meeting research (Phase 5)
│   └── pull-servicetitan-data.md      ← Extract job/revenue data (Phase 6)
│
└── templates/
    ├── pillar-brief.md                ← Template for pillar campaign briefs (Phase 5)
    └── campaign-report.md             ← Template for performance reports (Phase 5)
```

## How to Use a Workflow

1. **Start with the role workflow** — Read the relevant role file (e.g., `social-media.md`) to understand responsibilities, available tools, and context
2. **Find the task** — The role workflow links to specific task workflows for each operation
3. **Follow the task SOP** — Task workflows define inputs, steps, expected outputs, and edge cases
4. **Use the right tools** — Each workflow lists available tools in priority order (CLI → MCP → Python script)

## Current Status

| Role Workflow | Status | Task Workflows |
|--------------|--------|----------------|
| `social-media.md` | ✅ Complete | 3 task workflows |
| `ppc.md` | ✅ Complete | 2 task workflows |
| `email-marketing.md` | ✅ Complete | 2 task workflows |
| `content-strategy.md` | ✅ Complete | 3 task workflows + 2 templates |
| `lead-generation.md` | ✅ Complete | 1 task workflow |

## Key References

- [WAT Framework](../WAT_framework.md) — Core architecture and agent instructions
- [AI Guidelines](../anderson-lock-and-safe-ai-guidelines.md) — Brand voice, values, audience
- [Pillar Content Pipeline](../Pillar%20Content%20Pipeline%20-%20Architecture%20Plan.md) — The north-star system design
- [Engagement Calendar](../engagement-posts-calendar-apr-may-2026.md) — Active social content calendar
- [Marketing Roadmap](../Anderson%20Lock%20and%20Safe%20Marketing%20Roadmap.md) — Department roles and responsibilities
