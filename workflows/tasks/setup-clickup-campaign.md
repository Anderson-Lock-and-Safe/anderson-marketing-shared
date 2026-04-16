# Setup ClickUp Campaign — Task Workflow

## Objective

Create new pillar campaign tasks within the existing ClickUp Marketing Department Agent space. The structure is already built — this workflow is for populating it with campaign content.

## ClickUp Structure (Live)

**Space:** Marketing Department Agent (ID: `90144580877`)
**Workspace ID:** `9014302099`

```
Marketing Department Agent
│
├── 🧠 Strategy & Intel (Folder: 90147860704)
│   ├── Directives (901414572623)        — Standing Q2 priorities and strategic goals
│   ├── Campaign Briefs (901414572624)   — Pillar briefs for upcoming months
│   └── Competitive Intel (901414572625) — Market research and competitor notes
│
├── ✍️ Content Production (Folder: 90147860706)
│   ├── Content Queue (901414572627)     — Posts/emails waiting to be created
│   ├── Content Calendar (901414572629)  — Scheduled content with dates
│   └── Published Archive (901414572630) — Completed/published content
│
├── 📢 Campaigns (Folder: 90147860707)
│   ├── Active Campaigns (901414572631)  — Currently running campaigns and audits
│   └── Campaign Archive (901414572633)  — Completed campaigns
│
├── 🌐 Digital & SEO (Folder: 90147860708)
│   ├── Landing Pages (901414572634)     — Swipe Pages copy kits
│   └── Blog Posts (901414572635)        — SEO content drafts
│
├── 📊 Analytics & Reports (Folder: 90147860709)
│   ├── Weekly Reports (901414572636)    — PPC digests, performance reports
│   └── Attribution Tracking (901414572637) — ServiceTitan revenue matching
│
├── 👥 Sales & Outreach (Folder: 90147860710)
│   ├── Apollo Sequences (901414572638)  — Cold outreach campaigns
│   └── Sales Briefings (901414572639)   — Talking points and enablement
│
├── 🎥 Video & Creative (Folder: 90147860711)
│   ├── Video Briefs (901414572640)      — DropKick assignments
│   └── Asset Library (901414572641)     — Brand assets and templates
│
└── 📚 Story Library (901414572642)      — Customer stories and case studies
```

## Available Tools

| Priority | Tool | Purpose |
|----------|------|---------|
| 1 (MCP) | **ClickUp** — `clickup_create_task` | Create tasks in any list |
| 1 (MCP) | **ClickUp** — `clickup_filter_tasks` | Find existing tasks |
| 1 (MCP) | **ClickUp** — `clickup_update_task` | Update status, assignees, due dates |
| 1 (MCP) | **ClickUp** — `clickup_create_list_in_folder` | Add new lists for campaigns |
| 2 (Script) | `tools/bulk_clickup_tasks.py` | Batch create 30+ tasks (when built) |

## Per-Campaign Setup (Pillar Content)

When a pillar brief is approved, distribute content tasks across the existing structure:

### Step 1: Create the Brief
- **Where:** Campaign Briefs (`901414572624`)
- **Task name:** `YYYY-MM — [Topic Name] Pillar Brief`
- **Content:** Full brief using `workflows/templates/pillar-brief.md`

### Step 2: Create Content Tasks
Distribute across the appropriate lists:

| Content Type | List | Example Task Name |
|-------------|------|------------------|
| Email 1–4 | Content Queue (`901414572627`) | `[June Pillar] Email 1 — Problem Awareness` |
| LinkedIn posts (8) | Content Queue (`901414572627`) | `[June Pillar] LinkedIn 3 — Customer Pain Point` |
| Facebook posts (8) | Content Queue (`901414572627`) | `[June Pillar] Facebook 2 — Behind the Scenes` |
| Blog post | Blog Posts (`901414572635`) | `[June Pillar] Blog — Key Control Best Practices` |
| PPC ad copy | Active Campaigns (`901414572631`) | `[June Pillar] PPC Ad Copy Set` |
| Landing page | Landing Pages (`901414572634`) | `[June Pillar] Landing Page — Key Audit CTA` |
| Apollo sequence | Apollo Sequences (`901414572638`) | `[June Pillar] Apollo — Property Manager Outreach` |
| SMS messages | Content Queue (`901414572627`) | `[June Pillar] SMS 1 — Key Audit Reminder` |
| Video brief | Video Briefs (`901414572640`) | `[June Pillar] Video — 60s Key Control Explainer` |
| GBP posts | Content Queue (`901414572627`) | `[June Pillar] GBP — Phoenix Location Update` |
| CSR talking points | Sales Briefings (`901414572639`) | `[June Pillar] CSR Script — Key Control Theme` |

### Step 3: Set Task Details
Each task should include:
- **Description:** Full content copy
- **Due date:** Scheduled publish date
- **Priority:** Based on channel importance
- **Tags:** pillar name, channel, month (when tags are configured)

## Status Flow

Tasks move through ClickUp statuses:
```
Open → In Progress → Review → Approved → Scheduled → Complete
```

## Edge Cases

- **If ClickUp API rate limits are hit during bulk creation,** add delays between calls (~100 requests/minute limit).
- **Content that needs assets (Instagram, video)** should be created with a note in the description flagging the asset requirement and assigned to the appropriate creator.
- **Don't duplicate tasks.** Before creating, check `clickup_filter_tasks` for existing tasks with similar names in the target list.
