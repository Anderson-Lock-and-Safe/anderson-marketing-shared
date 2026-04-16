# Content Strategy / SEO Manager — Role Workflow

## Objective

Own the pillar content system: run monthly brainstorming sessions, generate full content kits from approved briefs, and coordinate the 2-month-ahead production pipeline described in the Pillar Content Pipeline doc.

## The System

See `Pillar Content Pipeline - Architecture Plan.md` for the full architecture. Summary:

```
Month 1: Brainstorm → Pick 2 pillar topics for Month 3
Month 2: Generate content kit → Review/approve → Distribute
Month 3: Content goes live → Monitor → Report
```

**You're always planning 2 months ahead.** This gives DropKick, freelancers, and the system enough runway.

## Monthly Rhythm

| When | What | Who |
|------|------|-----|
| **1st of month** | Monthly brainstorming session — present topic ideas, collaborate with Garrett, finalize 2 pillars | You + Garrett |
| **Days 3-5** | Generate full content kit for each pillar (30-35 tasks per pillar) | Content Engine (automated) |
| **Days 5-12** | Garrett reviews/approves content in ClickUp | Garrett |
| **Days 5-20** | Asset creation — DropKick (video), freelancer (graphics), Garrett (landing pages) | External |
| **Days 15-25** | Distribute approved content to platforms via MCP tools | Automated |
| **Day 15** | Mid-campaign analysis on currently-live content | You |
| **Day 30** | End-of-campaign report → feeds next brainstorm | You |

## Available Tools

| Priority | Tool | Purpose |
|----------|------|---------|
| 1 (MCP) | **ClickUp** | Command center — create campaign lists, tasks, track status |
| 2 (MCP) | **Buffer** | Schedule social posts from content kit |
| 3 (MCP) | **Klaviyo** | Create email campaigns from content kit |
| 4 (MCP) | **Google Ads / Bing / Meta / LinkedIn** | Upload ad copy from content kit |
| 5 (MCP) | **Apollo** | Create cold outreach sequences from content kit |
| 6 (MCP) | **ServiceTitan** | Pull revenue/job data for brainstorm prep |
| 7 (MCP) | **Windsor.ai** | Cross-platform performance data for analysis |
| 8 (Script) | `tools/bulk_clickup_tasks.py` | Batch create 30+ ClickUp tasks from content kit |
| 9 (Script) | `tools/content_kit_generator.py` | Orchestrate full content kit generation |

## Task Workflows

| Task | Workflow | When to Use |
|------|----------|-------------|
| Prepare for monthly brainstorm | [monthly-brainstorm-prep.md](tasks/monthly-brainstorm-prep.md) | Run before the 1st-of-month session |
| Generate full content kit | [generate-content-kit.md](tasks/generate-content-kit.md) | After a pillar brief is approved |
| Set up ClickUp campaign structure | [setup-clickup-campaign.md](tasks/setup-clickup-campaign.md) | Creating the ClickUp lists/tasks for a pillar |

## Templates

| Template | Purpose |
|----------|---------|
| [pillar-brief.md](templates/pillar-brief.md) | Standard format for pillar campaign briefs |
| [campaign-report.md](templates/campaign-report.md) | Standard format for end-of-campaign analysis |

## Content Kit Output (Per Pillar)

When a pillar brief is approved, the content engine generates:

| Channel | Pieces | Details |
|---------|--------|---------|
| **Email (Klaviyo)** | 4 emails | Problem awareness → Education → Social proof → CTA |
| **LinkedIn (organic)** | 8 posts | Mix: thought leadership, stats, pain points, CTAs |
| **Facebook/IG (organic)** | 8 posts | More visual/approachable tone |
| **Blog/SEO** | 1-2 posts | 800-1200 words, keyword-optimized |
| **PPC Ad Copy** | 3-5 sets | Headlines + descriptions for Google and Bing |
| **Landing Page** | 1 page | Full copy kit for Swipe Pages |
| **Apollo (cold email)** | 3-email sequence | Personalized outreach |
| **SMS** | 2-3 messages | Short, CTA-driven, complement emails |
| **Video Brief** | 1-2 briefs | For DropKick — concept, script, shot list |
| **GBP Posts** | 2-4 posts | Google Business Profile updates |
| **CSR Talking Points** | 1 doc | Internal — reinforce pillar message on calls |

**Total: ~30-35 ClickUp tasks per pillar, ~60-70 per month (2 pillars)**

## Edge Cases

- **If Garrett can't do the brainstorm on the 1st,** the prep work is still valuable. Reschedule within the first week.
- **If a pillar brief gets rejected,** don't generate the content kit. Go back to brainstorming for that slot.
- **If content kit quality is below 80% usable,** tune the generation prompts before running the next kit. Document what was weak in the workflow.
- **DropKick and freelancer work is external** — we create the briefs and assignments in ClickUp, but we don't control their timeline. Build in buffer for delays.
