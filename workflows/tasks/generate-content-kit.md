# Generate Content Kit — Task Workflow

## Objective

Take an approved pillar brief and generate the full content kit: ~30-35 individual content pieces across all channels, formatted and ready for review.

## Required Inputs

| Input | Source | Example |
|-------|--------|---------|
| **Pillar brief** | ClickUp task or `templates/pillar-brief.md` | Approved brief with topic, audience, CTA, key points |
| **Target month** | The month content goes live | June 2026 |
| **Brand guidelines** | `anderson-lock-and-safe-ai-guidelines.md` | Tone, values, restrictions |

## Steps

### 1. Read and Internalize the Brief

Read the full pillar brief. Understand:
- Core message
- Target audience segment
- Primary CTA
- Key points (3-5)
- Tone directive
- Any specific offers
- How it connects to previous campaigns

Read `anderson-lock-and-safe-ai-guidelines.md` for brand voice.

### 2. Generate Email Sequence (4 emails)

Follow the structure from `create-klaviyo-campaign.md`:

| Email | Week | Purpose | Tone |
|-------|------|---------|------|
| 1 | Week 1 | Problem awareness | Empathetic, questioning |
| 2 | Week 2 | Education/authority | Authoritative, helpful |
| 3 | Week 3 | Social proof/case study | Confident, specific |
| 4 | Week 4 | CTA/Offer | Urgent but not pushy |

Each email includes: 3 subject line options, preview text, full body copy, CTA button text + URL.

### 3. Generate LinkedIn Posts (8 posts)

2 per week across the month. Mix of:
- Thought leadership (industry insight from the pillar topic)
- Stat/fact (relevant data point with commentary)
- Customer pain point (problem the audience relates to)
- CTA (soft — "DM us" or "link in comments")
- Behind-the-scenes (team, process, expertise)

Professional but approachable tone. Include hashtag suggestions. Include visual direction notes.

### 4. Generate Facebook/IG Posts (8 posts)

2 per week. More visual/approachable tone than LinkedIn.
- Carousel ideas
- Reel concepts
- Single image posts
- Stories concepts

Include caption + visual direction for each. Note which ones need image assets.

### 5. Generate Blog Post (1-2 posts)

800-1200 words, SEO-optimized:
- Target keywords (research based on pillar topic)
- Meta description
- Title tag (under 60 chars)
- H2/H3 structure
- Internal linking suggestions
- CTA at the end

### 6. Generate PPC Ad Copy (3-5 variations)

For Google Ads and Bing Ads:
- Responsive Search Ad format: 15 headlines (30 chars max each), 4 descriptions (90 chars max each)
- Sitelink suggestions (4-6)
- Mapped to relevant keyword themes from the pillar topic

### 7. Generate Landing Page Copy (1 page)

For Swipe Pages:
- Headline + subheadline
- 3-4 body sections (problem, solution, proof, CTA)
- Social proof section (testimonials, stats)
- FAQ section (3-5 questions)
- CTA button text

### 8. Generate Apollo Cold Email Sequence (3 emails)

Targeted at the pillar's audience segment:
- Email 1: Introduction + value prop (Day 1)
- Email 2: Follow-up + case study angle (Day 3)
- Email 3: Final touch + direct CTA (Day 7)

Include personalization token suggestions, subject lines, and body copy.

### 9. Generate SMS Messages (2-3)

Short, CTA-driven, timed to complement email sequence:
- Under 160 characters each
- Include opt-out language
- Clear action: call, book, visit URL

### 10. Generate Video Brief (1-2)

For DropKick:
- Concept/hook (first 3 seconds)
- Script outline or talking points
- Shot suggestions
- Target length (30s, 60s, or 90s)
- Where it'll be used (social, website, email, ads)
- Reference footage if available

### 11. Generate GBP Posts (2-4)

Google Business Profile updates tied to the pillar theme:
- Short, local-focused
- Include CTA (call, visit website, get directions)

### 12. Generate CSR Talking Points (1 doc)

Internal document for Customer Service Representatives:
- 2-3 sentence summary of this month's pillar theme
- Script snippet for reinforcing the message on calls
- Key offers/promotions to mention
- FAQ for common customer questions about the topic

### 13. Create ClickUp Tasks

Using `tools/bulk_clickup_tasks.py` (or ClickUp MCP tools directly):
- Create a list under PILLAR CAMPAIGNS for this campaign (e.g., "2026-06 Key Control")
- Create one task per content piece with:
  - Task name (e.g., "Email 1 — Problem Awareness")
  - Channel custom field
  - Content Status: Draft
  - Scheduled Date
  - Copy (full content in the task description)
  - Visual Direction (where applicable)

## Quality Checks

Before delivering the kit, verify each piece:
- [ ] On-brand per AI guidelines
- [ ] Correct audience (commercial, not residential)
- [ ] CTA is clear and consistent with the pillar brief
- [ ] No conflicting messages between channels
- [ ] Tone matches platform (casual FB, professional LI, etc.)
- [ ] Scheduled dates don't conflict with holidays or company events
- [ ] Each piece can stand alone (not everyone sees every touchpoint)

## Expected Output

~30-35 content pieces organized by channel, all populated as ClickUp tasks under the campaign list.

## Edge Cases

- **If the brief is vague on audience,** default to the broadest commercial segment (property managers + facilities teams) and note the assumption.
- **If the brief includes an offer/discount,** verify the terms are approved before including in content. Flag for Garrett if unclear.
- **If Instagram content is included,** note that image/video assets are required. Create the caption and visual direction, but flag that assets need to be produced.
- **Blog post requires WordPress** — if WordPress isn't set up yet, create the content anyway and store in ClickUp for when it's ready.
