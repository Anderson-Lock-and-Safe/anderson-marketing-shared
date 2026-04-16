# Generate Engagement Post — Task Workflow

## Objective

Generate a single social media engagement post from the content calendar for a specific date and platform.

## Required Inputs

| Input | Source | Example |
|-------|--------|---------|
| **Date** | From content calendar or user request | `Mon Apr 27` |
| **Platform** | `facebook` or `linkedin` | `linkedin` |
| **Content Calendar** | `engagement-posts-calendar-apr-may-2026.md` | Week 2, Mon Apr 27 row |

## Steps

### 1. Read the Content Calendar
Open `engagement-posts-calendar-apr-may-2026.md` and find the row for the requested date.

Extract:
- **Topic** (e.g., "Key control awareness")
- **Platform-specific direction** (the Facebook column or LinkedIn column)

### 2. Read Brand Guidelines
Reference `anderson-lock-and-safe-ai-guidelines.md` for tone, values, and restricted content.

### 3. Generate the Post

**Facebook posts should:**
- Be conversational, first-person, relatable
- Use casual language ("we've all been there", "raise your hand if...")
- Include a clear question to drive comments
- 1-3 short paragraphs max
- No hashtags (or minimal — 1-2 max)
- End with a question or call to engage

**LinkedIn posts should:**
- Lead with expertise and industry knowledge
- Reference specific commercial contexts (property management, facilities, multi-unit)
- Mention Anderson Lock and Safe's 60+ year track record where natural
- Be professional but not stiff
- 2-4 paragraphs
- Include 3-5 relevant hashtags at the end
- End with a question to drive professional discussion

### 4. Format the Output

```
PLATFORM: [Facebook / LinkedIn]
DATE: [Scheduled date]
TOPIC: [Topic from calendar]

---

[Post copy here]

---

HASHTAGS: [LinkedIn only — 3-5 hashtags]
VISUAL DIRECTION: [Brief note on what image would complement this post, if any]
```

### 5. Quality Check

Before finalizing, verify:
- [ ] Does NOT lead with a hard sell or CTA
- [ ] Asks a genuine question that invites engagement
- [ ] Demonstrates expertise through specificity (not generic)
- [ ] Matches the platform tone (casual for FB, professional for LI)
- [ ] Does NOT focus on residential locksmithing
- [ ] Does NOT compete on price
- [ ] Length is appropriate (FB: shorter/punchier, LI: can be longer)

## Expected Output

Ready-to-schedule post copy with platform, date, and optional visual direction notes.

## Edge Cases

- **If the calendar entry is vague,** expand it using the topic and the platform tone guidelines. The calendar provides direction, not exact copy.
- **If the date has already passed,** note this and ask whether to generate anyway (for backfill) or skip.
- **If generating for both platforms at once,** produce two separate posts with distinct angles — never just copy/paste and adjust tone.
