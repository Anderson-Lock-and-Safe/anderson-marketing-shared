# Audit Klaviyo Flows — Task Workflow

## Objective

Audit the current state of all Klaviyo flows and email performance. Diagnose the 0.14% click rate problem. Assess the 3 dormant flows (win-back, review request, re-engagement) and prepare them for reactivation.

## Required Inputs

None — this workflow pulls everything it needs from Klaviyo directly.

## Steps

### 1. Get Account Overview

Using Klaviyo MCP tools:
- List all flows — capture name, status (live/draft/manual/dormant), trigger type
- List all lists and segments — capture name, member count, type
- Pull recent campaign performance — last 10-20 campaigns with open rate, click rate, bounce rate, unsubscribe rate

### 2. Assess List Health

| Metric | Healthy | Warning | Critical |
|--------|---------|---------|----------|
| **Bounce rate** | < 2% | 2-5% | > 5% |
| **Unsubscribe rate** | < 0.5% | 0.5-1% | > 1% |
| **Open rate** | > 20% | 15-20% | < 15% |
| **Click rate** | > 2% | 1-2% | < 1% (we're at 0.14%) |
| **Spam complaint rate** | < 0.1% | 0.1-0.3% | > 0.3% |

Check:
- Total list size vs engaged subscribers (opened/clicked in last 90 days)
- Percentage of list that hasn't engaged in 6+ months
- Any suppressed or bounced contacts that should be cleaned

### 3. Diagnose Click Rate

Walk through the diagnosis framework from `email-marketing.md`:

1. **List health:** What % of the list is unengaged? If > 40%, recommend list cleaning.
2. **Segmentation:** Are campaigns sent to the full list or segments? Pull recent campaign recipient counts.
3. **Content audit:** Read the last 5 campaign emails. Are CTAs clear, above the fold, and relevant to commercial audiences?
4. **Subject line performance:** Compare open rates across campaigns. Patterns?
5. **Deliverability signals:** Bounce rate trend, spam complaints, any blacklist indicators.
6. **Send frequency:** How often are campaigns sent? When was the last one?

### 4. Audit Dormant Flows

For each of the 3 dormant flows (win-back, review request, re-engagement):

Check:
- **Trigger:** What event triggers this flow? Is the trigger still valid?
- **Content:** Read the email content in the flow. Is it on-brand per current guidelines?
- **Filters/Conditions:** Are there segment filters that might prevent triggering?
- **Last active date:** When did it stop? Any errors or reasons it was paused?
- **Email count:** How many emails in the sequence? Timing between them?

For each flow, assess:
- **Safe to reactivate as-is?** Or does content need updating first?
- **Are trigger events still firing?** (e.g., does ServiceTitan still send the right data to Klaviyo?)
- **Expected volume:** How many people would enter this flow if activated today?

### 5. Generate Audit Report

```
## Klaviyo Audit Report — [Date]

### Account Overview
- Total profiles: X
- Active subscribers: X
- Engaged (90 days): X (X%)
- Unengaged (90+ days): X (X%)
- Total flows: X (Y active, Z dormant, W draft)
- Total lists/segments: X

### Click Rate Diagnosis
**Current:** 0.14% | **Industry Avg:** 2.6% | **Gap:** 18.6x below average

**Root Causes Identified:**
1. [Primary cause with evidence]
2. [Secondary cause with evidence]
3. [Contributing factor]

**Recommended Fix Priority:**
1. [Most impactful fix — expected improvement]
2. [Second fix]
3. [Third fix]

### Flow Status

| Flow | Status | Trigger | Emails | Last Active | Recommendation |
|------|--------|---------|--------|-------------|----------------|
| Win-Back | Dormant | ... | ... | Jul 2025 | ... |
| Review Request | Dormant | ... | ... | Jul 2025 | ... |
| Re-Engagement | Dormant | ... | ... | Jul 2025 | ... |
| [Other flows] | ... | ... | ... | ... | ... |

### Flow Reactivation Plan
**Win-Back:**
- Content update needed: [yes/no, what specifically]
- Trigger still valid: [yes/no]
- Safe to reactivate: [yes/no/after updates]

**Review Request:**
- [Same structure]

**Re-Engagement:**
- [Same structure]

### List Cleaning Recommendation
- Profiles to suppress/remove: X
- Criteria: [e.g., no opens in 180 days, bounced, etc.]
- Expected impact on click rate: [estimate]

### Next Steps
1. [Specific action with owner]
2. [Specific action with owner]
3. [Specific action with owner]
```

### 6. Deliver

- Output report directly to user
- Create ClickUp task in PERFORMANCE folder with the report
- If critical issues found, also send summary to Google Chat

## Edge Cases

- **If Klaviyo MCP tools can't access flow details,** document what's accessible and what needs to be checked in the Klaviyo UI manually.
- **If flows reference integrations that are no longer connected,** flag this — reactivating a flow with a broken trigger will silently fail.
- **Don't reactivate flows without Garrett's approval.** This audit diagnoses and recommends. Activation is a separate step.
