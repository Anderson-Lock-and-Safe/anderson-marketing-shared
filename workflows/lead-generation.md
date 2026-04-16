# Lead Generation — Role Workflow

## Objective

Drive new business through cold outreach (Apollo) and data-driven targeting using ServiceTitan job and revenue data. Supplement the inbound marketing engine with proactive outbound to high-value commercial prospects.

## Available Tools

| Priority | Tool | Purpose |
|----------|------|---------|
| 1 (MCP) | **Apollo** | Lead prospecting, enrichment, cold email sequences. 10,510 lead credits remaining. |
| 2 (MCP) | **ServiceTitan** | Customer data, job history, revenue by type — informs targeting |
| 3 (MCP) | **ClickUp** | Track outreach campaigns and results |
| 4 (MCP) | **Klaviyo** | Warm lead nurture after initial Apollo engagement |

## Apollo Strategy

### Target Segments (Commercial Focus)

Based on Anderson Lock's target audience, prioritize outreach to:

| Segment | Why | Apollo Filters |
|---------|-----|---------------|
| Property Management Companies | High volume, recurring work | Industry: Real Estate, Title: Property Manager / Facilities Director |
| General Contractors | Project-based, high-value | Industry: Construction, Title: Project Manager / Superintendent |
| School Districts | Large accounts, seasonal needs | Industry: Education, Title: Facilities Director / Operations Manager |
| Healthcare Facilities | Security-critical, compliance-driven | Industry: Healthcare, Title: Facilities Manager / Security Director |
| Government Entities | Large contracts, reliable payment | Industry: Government, Title: Procurement / Facilities |
| Multi-Family Housing | Master key systems, rekeying volume | Industry: Real Estate, Title: Maintenance Director |

### Outreach Sequence Structure

Standard 3-email sequence (aligned with pillar campaign themes when applicable):

| Email | Timing | Purpose |
|-------|--------|---------|
| Email 1 | Day 1 | Introduction + specific value prop for their industry |
| Email 2 | Day 3 | Follow-up + proof point (case study, stat, guarantee) |
| Email 3 | Day 7 | Final touch + direct CTA (call, meeting, site visit) |

**Personalization tokens:** Company name, industry, title, local context (Phoenix metro area)

### Apollo Credits Management

- **10,510 lead credits remaining** — use strategically
- Prioritize quality over quantity — enrich leads before sequencing
- Track credits used per campaign for budget awareness
- If credits run low, flag for Garrett before continuing outreach

## ServiceTitan Data Usage

### What to Pull

| Data | Purpose |
|------|---------|
| Revenue by job type (90 days) | Identify high-margin service categories to promote |
| Customer list by industry | Find similar prospects in Apollo |
| Job completion data | Identify successful project types for case studies |
| New vs. repeat customer ratio | Measure retention and acquisition balance |
| Geographic distribution | Focus outreach on highest-value service areas |

### How to Use It

1. **Inform targeting:** If access control jobs are growing 40% YoY, target prospects who need access control
2. **Build case studies:** Use completed project data to create proof points for outreach
3. **Identify gaps:** If a segment (e.g., schools) has low penetration but high revenue potential, prioritize outreach there
4. **Seasonal timing:** If certain job types spike seasonally, time outreach 30-60 days ahead

## Task Workflows

| Task | Workflow | When to Use |
|------|----------|-------------|
| Extract ServiceTitan data | [pull-servicetitan-data.md](tasks/pull-servicetitan-data.md) | Monthly, before brainstorming and outreach planning |

## Weekly Rhythm

| Day | Action |
|-----|--------|
| **Monday** | Check Apollo sequence performance (open rates, reply rates) |
| **Wednesday** | Review any replies — flag hot leads for Garrett to follow up |
| **Friday** | Enrich and queue next batch of prospects if sequences are running |
| **End of Month** | Report: leads generated, sequences sent, reply rate, meetings booked |

## Edge Cases

- **Apollo replies require human follow-up.** Flag warm replies for Garrett immediately. Don't try to automate the conversation beyond the initial sequence.
- **If a lead is already an Anderson Lock customer** (check against ServiceTitan), remove from Apollo sequence. Don't cold-email existing clients.
- **CAN-SPAM compliance:** All emails must include company info and unsubscribe option. Apollo handles this, but verify.
- **Credit conservation:** If a campaign isn't getting results after 200 sends with < 1% reply rate, pause and reassess the targeting or messaging before burning more credits.
