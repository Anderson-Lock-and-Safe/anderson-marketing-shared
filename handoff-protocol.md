# Task Handoff Protocol

When Garrett redirects a task to a different agent (via comment or status change), or when you determine a task belongs to another agent, follow this protocol.

## How to Hand Off a Task

1. **Add a handoff comment** to the ClickUp task:
```
🔄 HANDOFF → [Receiving Agent Name]

**Reason:** [Why this task is being redirected — Garrett's feedback or your assessment]

**Work Completed So Far:**
- [What you did]
- [Assets identified/analyzed]
- [Drafts created (include IDs)]
- [Key findings]

**Context for Receiving Agent:**
- [What they need to know to pick this up without starting over]
- [Any relevant file IDs, URLs, analysis results]

**Recommendation:** [What you think the receiving agent should do with this]
```

2. **Clean up your work** — delete any Buffer drafts, cancel any pending actions
3. **Update the Agent custom field** to the receiving agent
4. **Set status to "Open"** so the receiving agent picks it up fresh

## Agent Custom Field

**Field ID:** `20572024-c406-4299-91b3-2a4934837a7a`

| Agent | Option ID |
|-------|-----------|
| PPC Specialist | `2bb6a2cf-31bf-4cf6-af84-0f72892c57e6` |
| Social Media Manager | `5d30dbd1-f0a8-42e4-b49b-2b8057b691c5` |
| Email Marketing Specialist | `6d7f23c3-1578-430c-8076-d08a962b4ab1` |
| Content Strategist | `0a216f71-47ad-4fe4-b7be-e48f26131b05` |
| Lead Gen Specialist | `117d113e-ef08-4ec2-9d14-951d20c12a79` |

## Common Handoff Scenarios

| From | To | Example Trigger |
|------|-----|----------------|
| Social Media → PPC | "This would work better as a paid ad" |
| Social Media → Content Strategist | "This needs a full content kit, not a single post" |
| PPC → Social Media | "Turn this high-performing ad into organic content" |
| Content Strategist → Social Media | "Content kit approved, schedule the social posts" |
| Content Strategist → Email Marketing | "Content kit approved, create the Klaviyo campaigns" |
| Content Strategist → Lead Gen | "Content kit approved, set up the Apollo sequence" |
| Email Marketing → Content Strategist | "This flow needs new content written" |
| Any → Any | Garrett reassigns via Agent dropdown in ClickUp |

## Receiving a Handoff

When you pick up a task that was handed off from another agent:
1. Read the handoff comment first — it has all the context
2. Don't redo work that's already been done (assets identified, analysis completed, etc.)
3. Start your work from where the previous agent left off
4. Post a starting comment acknowledging the handoff: `🔄 Picked up from [Previous Agent]. Starting from [their last step].`
