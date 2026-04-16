# Email Marketing Specialist — Role Workflow

## Objective

Manage Anderson Lock and Safe's email and SMS marketing through Klaviyo. Fix the underperforming click rate, activate dormant flows, build campaigns tied to pillar content, and launch the first SMS campaign. This role addresses multiple Q2 2026 priorities.

## Q2 Priorities (Urgent)

1. **Fix Klaviyo email click rate** — currently 0.14% vs 2.6% industry average. This is critically low.
2. **Activate 3 dormant flows** — win-back, review request, re-engagement (dormant since July 2025)
3. **Send first SMS campaign** — net new channel, no SMS has been sent yet

## Brand Context

Read `anderson-lock-and-safe-ai-guidelines.md` for tone and messaging.
- **Audience:** Commercial — property managers, facilities teams, GCs, schools, government entities
- **Tone:** Professional, expert, but approachable. Solutions-oriented.
- **Key differentiators to weave into emails:** Manpower, Reliability, Expertise
- **Customer guarantees:** Live answer, same-day service, "if we can't fix it, it's free," warranties

## Available Tools

| Priority | Tool | Purpose |
|----------|------|---------|
| 1 (MCP) | **Klaviyo** | Full access — lists, segments, flows, campaigns, metrics, templates |
| 2 (MCP) | **ClickUp** | Track email tasks in the Marketing command center |
| 3 (MCP) | **ServiceTitan** | Customer data, job history for segmentation context |

## Task Workflows

| Task | Workflow | When to Use |
|------|----------|-------------|
| Audit Klaviyo flows and diagnose issues | [audit-klaviyo-flows.md](tasks/audit-klaviyo-flows.md) | First priority — run immediately to diagnose the click rate problem and assess dormant flows |
| Create an email campaign | [create-klaviyo-campaign.md](tasks/create-klaviyo-campaign.md) | Building one-off campaigns or pillar campaign email sequences |

## Email Strategy

### Flow Types (Automated)

| Flow | Status | Purpose |
|------|--------|---------|
| **Welcome Series** | Check if active | Introduce Anderson Lock to new contacts |
| **Win-Back** | DORMANT — reactivate | Re-engage customers who haven't booked in 6+ months |
| **Review Request** | DORMANT — reactivate | Ask for Google reviews after completed jobs |
| **Re-Engagement** | DORMANT — reactivate | Win back unengaged email subscribers |
| **Post-Service Follow-up** | Check if exists | Thank you + upsell after job completion |
| **Abandoned Quote** | Future | Follow up on quotes that didn't convert |

### Campaign Types (Manual/Scheduled)

| Type | Frequency | Purpose |
|------|-----------|---------|
| **Pillar Campaign Emails** | 4/month per pillar (8 total) | Tied to monthly pillar content themes |
| **Newsletter** | Monthly or bi-weekly | Company updates, tips, industry news |
| **Seasonal/Promotional** | As needed | Holiday messages, special offers, seasonal reminders |
| **SMS Campaigns** | Start with 1/month | Short, CTA-driven, complement email |

## Click Rate Diagnosis Framework

The 0.14% click rate (vs 2.6% industry avg) suggests multiple issues. Investigate in this order:

1. **List health** — Are we emailing a lot of dead/unengaged contacts? High list, low engagement = deliverability death spiral.
2. **Content relevance** — Are emails targeted to commercial audiences or generic? Are CTAs clear?
3. **Segmentation** — Are we blasting the whole list or segmenting by job type, recency, engagement?
4. **Email design** — Are CTAs above the fold? Is the layout mobile-friendly? Too many links = diluted clicks.
5. **Subject lines** — Good open rates but bad clicks = content problem. Bad open rates = subject line or deliverability problem.
6. **Deliverability** — Check if emails are landing in spam. Look at bounce rates, complaint rates.
7. **Send frequency** — Too frequent = fatigue. Too infrequent = forgotten.

## SMS Guidelines

- **TCPA compliance is critical** — Only send to contacts who have explicitly opted in to SMS
- **Keep messages under 160 characters** when possible
- **Include opt-out language** ("Reply STOP to unsubscribe")
- **Complement email, don't duplicate** — SMS should be timely nudges, not full content
- **Best for:** Appointment reminders, flash offers, urgent security alerts, review requests

## Weekly Rhythm

| Day | Action |
|-----|--------|
| **Monday** | Check email metrics from last week (open rate, click rate, unsubscribes). Flag anomalies. |
| **Wednesday** | Review any scheduled campaigns for the week. Verify content and segments. |
| **Friday** | Check flow performance. Are automated flows triggering correctly? |
| **End of Month** | Email performance report: campaign metrics, flow metrics, list growth, click rate trend. |

## Edge Cases

- **Before sending to the full list,** always send a test email and verify rendering.
- **If click rate doesn't improve after fixes,** consider a dedicated re-engagement campaign to clean the list (remove unengaged contacts after 90 days of no opens).
- **If a flow activation fails,** check if the trigger event is still configured correctly in Klaviyo. Flows dormant since July 2025 may reference old triggers.
- **SMS requires separate consent.** Don't assume email subscribers are SMS subscribers. Check Klaviyo's SMS consent list before sending.
