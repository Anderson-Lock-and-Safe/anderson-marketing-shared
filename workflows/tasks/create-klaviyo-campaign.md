# Create Klaviyo Campaign — Task Workflow

## Objective

Build and schedule an email campaign in Klaviyo, from copy creation through scheduling. Used for one-off campaigns and pillar campaign email sequences.

## Required Inputs

| Input | Source | Example |
|-------|--------|---------|
| **Campaign purpose** | User request or pillar brief | "April newsletter", "Key Control pillar - Email 1" |
| **Target segment** | Specific segment or default list | "All engaged subscribers", "Property managers" |
| **Send date** | User request or content calendar | `2026-04-28 10:00 AM MST` |
| **Content brief** | Pillar brief, user direction, or template | Topic, key points, CTA |

## Steps

### 1. Define the Email

Based on the brief, determine:
- **Subject line** — 3 options for A/B testing. Keep under 50 characters. Personalization tokens where appropriate.
- **Preview text** — Complements the subject line, doesn't repeat it. Under 100 characters.
- **Body copy** — Structured for commercial audience:
  - Hook (problem or question relevant to their business)
  - Value (how Anderson Lock solves it, with specificity)
  - Proof (stats, guarantees, experience)
  - CTA (clear, single action — call, book, get a quote)
- **CTA** — One primary CTA. Make it obvious and above the fold.

### 2. Apply Brand Voice

Reference `anderson-lock-and-safe-ai-guidelines.md`:
- Professional but approachable
- Solutions over problems
- Value over price
- Commercial focus (property managers, facilities teams, GCs)
- Include relevant guarantees (live answer, same-day, warranties)

### 3. Format the Email Content

```
CAMPAIGN NAME: [Descriptive name for Klaviyo]
SUBJECT LINE A: [Option 1]
SUBJECT LINE B: [Option 2]
SUBJECT LINE C: [Option 3]
PREVIEW TEXT: [Preview text]

---

[Email body copy — formatted with clear sections]

[Primary CTA button text: e.g., "Schedule Your Key Audit"]
[CTA link destination: e.g., landing page URL or phone number]

---

SEGMENT: [Target segment name]
SEND DATE: [Date and time with timezone]
A/B TEST: [Subject lines — send to 20% of list, winner to remaining 80%]
```

### 4. Create in Klaviyo

Using Klaviyo MCP tools:
1. Create the campaign with name, subject line, and segment
2. Set the send date/time
3. Configure A/B test if using multiple subject lines

### 5. Quality Check

Before scheduling:
- [ ] Subject line is under 50 characters
- [ ] Preview text doesn't repeat the subject line
- [ ] CTA is clear and above the fold
- [ ] Content is relevant to the target segment
- [ ] No residential focus — commercial audience only
- [ ] Send time is appropriate (Tuesday-Thursday 10am-2pm MST generally best for B2B)
- [ ] Unsubscribe link is present (Klaviyo handles this automatically)
- [ ] Reply-to address is correct

### 6. Schedule or Send Test

- **If ready:** Schedule for the target send date
- **If needs review:** Save as draft and create ClickUp task with status "Needs Review"
- **Always:** Send a test email to garrett@andersonlockandsafe.com first if this is a new template or format

## Pillar Campaign Email Sequence

When creating emails for a pillar campaign, follow this 4-email structure over the month:

| Email | Week | Purpose | Tone |
|-------|------|---------|------|
| Email 1 | Week 1 | Problem awareness — surface a pain point | Empathetic, questioning |
| Email 2 | Week 2 | Education — teach something valuable | Authoritative, helpful |
| Email 3 | Week 3 | Social proof — case study or testimonial | Confident, specific |
| Email 4 | Week 4 | CTA/Offer — direct ask with incentive | Urgent but not pushy |

Each email should reference the pillar theme but stand alone (not everyone opens every email).

## Edge Cases

- **If Klaviyo doesn't have an appropriate segment,** document what segment is needed and ask Garrett to create it (or create it via MCP if the tool supports it).
- **If the send list is very small (< 100),** flag this — small sends can skew A/B test results. Consider sending without A/B test.
- **If campaign references an offer or discount,** verify with Garrett that the offer is approved and the terms are correct.
- **Never send a campaign without a test email first** if it uses a new template or layout.
