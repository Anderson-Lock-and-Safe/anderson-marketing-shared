# Agent Architecture — Three-Tier Model

Every agent in the marketing department follows the same three-tier pattern. Only the top tier is triggered externally — it orchestrates the tiers below it.

## The Pattern

```
TIER 1: PLANNER (Opus)
  Triggered by: ClickUp task assignment, webhook, or schedule
  Does: Research, reasoning, strategy, task decomposition
  Outputs: ClickUp tasks with detailed briefs for Tier 2
  
TIER 2: CREATOR (Sonnet)  
  Triggered by: Tier 1 creates tasks with status "open"
  Does: Hands-on execution — writing, analyzing, building, drafting
  Outputs: Deliverables ready for review (drafts, reports, analysis)
  
TIER 3: EXECUTOR (Haiku)
  Triggered by: Garrett approves → task status changes to "Approved"
  Does: Simple, fast actions — publish, send, queue, update, move
  Outputs: Final confirmation, status set to "Complete"
```

## Why This Works

- **Opus thinks** — it's expensive but brilliant at research, pattern recognition, and strategic decisions. It touches each task once to plan, then gets out of the way.
- **Sonnet builds** — it's the workhorse. Fast enough to process multiple tasks, smart enough to write good copy and make creative decisions.
- **Haiku ships** — it's cheap and fast. Approving a draft into a queue doesn't need intelligence, it needs reliability.

## Cost Efficiency

| Tier | Model | When It Runs | Cost Profile |
|------|-------|-------------|-------------|
| Planner | Opus | Once per batch of work | High per-run, low frequency |
| Creator | Sonnet | Once per task | Medium per-run, medium frequency |
| Executor | Haiku | Once per approval | Very low per-run, medium frequency |

A typical post costs: ~$0.50 (Opus planning) + ~$0.10 (Sonnet creating) + ~$0.01 (Haiku publishing) = ~$0.61 per post.

## How Tasks Flow Between Tiers

```
Garrett creates task: "Make 5 posts for this week"
  │
  ▼
PLANNER (Opus) picks up the task
  ├── Researches: content library, ServiceTitan, web trends
  ├── Creates 5 individual ClickUp tasks with detailed briefs
  ├── Sets each to status "open", Agent = Social Media Manager  
  ├── Marks parent task "Complete"
  └── Exits
  
CREATOR (Sonnet) picks up each task on next run
  ├── Reads the brief from Planner
  ├── Analyzes the suggested asset (Gemini for video)
  ├── Writes the caption per brand guidelines
  ├── Creates a Buffer draft
  ├── Posts draft details to ClickUp
  ├── Sets status to "Review"
  └── Moves to next task (max 3 per run)

Garrett reviews each draft in ClickUp
  ├── Approve → sets status to "Approved"
  ├── Feedback → adds comment, Creator revises on next run
  └── Reject → sets status to "Closed"

EXECUTOR (Haiku) picks up approved tasks
  ├── Reads the Buffer draft ID from comments
  ├── Promotes draft to queue
  ├── Sets status to "Complete"
  └── Done
```

## Applying to Other Agents

This same pattern works for every marketing function:

### PPC Specialist
| Tier | Does |
|------|------|
| Planner (Opus) | Analyzes performance data, identifies optimization opportunities, creates task briefs |
| Creator (Sonnet) | Writes ad copy, generates negative keyword lists, drafts bid change recommendations |
| Executor (Haiku) | Applies approved bid changes, adds approved negative keywords |

### Email Marketing Specialist
| Tier | Does |
|------|------|
| Planner (Opus) | Audits flows, diagnoses click rate issues, plans campaign strategy |
| Creator (Sonnet) | Writes email copy, builds campaign drafts in Klaviyo |
| Executor (Haiku) | Activates approved flows, schedules approved campaigns |

### Content Strategist
| Tier | Does |
|------|------|
| Planner (Opus) | Monthly brainstorm research, topic selection, pillar brief creation |
| Creator (Sonnet) | Generates full content kits (30-35 pieces per pillar) |
| Executor (Haiku) | Creates ClickUp tasks for each content piece, distributes to other agents |

### Lead Gen Specialist
| Tier | Does |
|------|------|
| Planner (Opus) | Analyzes ServiceTitan data, identifies target segments, plans outreach strategy |
| Creator (Sonnet) | Writes outreach sequences, enriches prospect lists |
| Executor (Haiku) | Activates approved Apollo sequences |

## Trigger Chain

Only the Planner needs an external trigger. The rest are triggered by ClickUp task status:

```
External trigger → Planner runs → creates tasks (status: open)
                                        │
Scheduled check → Creator runs → picks up open tasks → sets to Review
                                        │
                              Garrett reviews/approves
                                        │
Scheduled check → Executor runs → picks up approved tasks → sets to Complete
```

## Routine Naming Convention

Each routine follows: `[Agent Name] - [Tier]`

Examples:
- `Social Media - Planner`
- `Social Media - Creator`  
- `Social Media - Publisher`
- `PPC - Planner`
- `PPC - Creator`
- `PPC - Executor`

## Environment Variables Per Agent

Each agent's cloud environment should have only the tokens it needs:

| Agent | Planner Env | Creator Env | Executor Env |
|-------|------------|-------------|-------------|
| Social Media | (none needed) | BUFFER_TOKEN, GEMINI_API_KEY | BUFFER_TOKEN |
| PPC | (none needed) | (none - uses MCP) | (none - uses MCP) |
| Email Marketing | (none needed) | (none - uses MCP) | (none - uses MCP) |
| Content Strategist | (none needed) | GEMINI_API_KEY | (none needed) |
| Lead Gen | (none needed) | (none - uses MCP) | (none - uses MCP) |
