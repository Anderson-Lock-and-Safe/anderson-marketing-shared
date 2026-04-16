# Optimize PPC Keywords — Task Workflow

## Objective

Review search terms, adjust keyword bids, add negative keywords, and identify new keyword opportunities across Google Ads and Microsoft/Bing Ads.

## Required Inputs

| Input | Source | Example |
|-------|--------|---------|
| **Platform** | User request or both by default | `google`, `bing`, `both` |
| **Campaign/Ad Group** | Specific or all | `all`, campaign ID, ad group ID |
| **Time period** | For search term data | `last 30 days` (recommended minimum) |

## Steps

### 1. Pull Search Terms

**Google Ads:**
```
Tool: gads_get_search_terms
Params: date_range (recommend 30 days for meaningful data)
```

**Bing Ads:**
```
Tool: msads_submit_report (search term report)
Then: msads_poll_report to get results
```

### 2. Categorize Search Terms

Review each search term and categorize:

| Category | Action | Example |
|----------|--------|---------|
| **Converting & relevant** | Keep, consider increasing bid | "commercial locksmith phoenix" |
| **Relevant but not converting** | Monitor, check landing page | "access control installation az" |
| **Irrelevant — residential** | Add as negative keyword | "house lockout", "car key replacement", "residential locksmith" |
| **Irrelevant — wrong intent** | Add as negative keyword | "locksmith salary", "how to pick a lock", "locksmith school" |
| **Irrelevant — wrong location** | Add as negative keyword | "locksmith los angeles", "locksmith near me" (if geo isn't Phoenix) |
| **New opportunity** | Consider adding as exact/phrase match keyword | Relevant terms not currently targeted |

### 3. Add Negative Keywords

For irrelevant terms identified:

**Google Ads:**
```
Tool: gads_add_negative_keyword
Params: campaign_id, keyword text, match_type
```

**Bing Ads:**
```
Tool: msads_add_negative_keyword
Params: campaign_id or ad_group_id, keyword text
```

**Important:** Add negatives at the campaign level unless the term is only irrelevant for specific ad groups.

### 4. Review Keyword Bids

Pull current keywords and performance:

**Google Ads:**
```
Tool: gads_list_keywords
Then: Cross-reference with performance data
```

**Bid Adjustment Guidelines:**
- **High conversion rate + low impression share** → Increase bid 10-20%
- **High cost + low conversion rate** → Decrease bid 15-25% or pause
- **Good CTR but no conversions** → Check landing page before changing bid
- **Very low CTR (< 1%)** → Review ad copy relevance, consider pausing keyword
- **Quality Score below 5** → Improve ad relevance and landing page experience

**Threshold for approval:** Changes over $5/keyword or affecting 10+ keywords at once → flag for Garrett.

### 5. Document Changes

For every change made, log:

```
## Keyword Optimization Log — [Date]

### Negative Keywords Added
| Platform | Campaign | Keyword | Match Type | Reason |
|----------|----------|---------|-----------|--------|
| Google   | ...      | ...     | ...       | ...    |

### Bid Adjustments
| Platform | Campaign | Keyword | Old Bid | New Bid | Reason |
|----------|----------|---------|---------|---------|--------|
| Google   | ...      | ...     | $X.XX   | $X.XX   | ...    |

### New Keywords Recommended (Pending Approval)
| Platform | Suggested Keyword | Match Type | Suggested Bid | Reasoning |
|----------|------------------|-----------|---------------|-----------|
| ...      | ...              | ...       | ...           | ...       |
```

### 6. Deliver

- Output log to user directly
- If part of weekly rhythm: create ClickUp task in PERFORMANCE folder

## Common Negative Keyword Categories for Anderson Lock

These should already be negated but verify periodically:

**Residential/Consumer:**
house, home, apartment, residential, car, auto, vehicle, garage door, door lock replacement DIY

**Wrong Intent:**
salary, training, school, certification, how to, DIY, pick a lock, youtube, reddit, free

**Wrong Location (unless Anderson expands):**
Cities outside Phoenix metro area

**Competitors (usually don't negate, but monitor):**
Competitor names — monitor search terms but usually don't negate unless the traffic is pure waste

## Edge Cases

- **Before adding negative keywords in bulk,** review the full list with Garrett if more than 20 negatives in one session — some terms may look irrelevant but actually convert.
- **Shared negative keyword lists:** Google supports shared lists across campaigns. Use these for universal negatives (residential, DIY, etc.) to avoid maintaining per-campaign lists.
- **Bing imports from Google:** Bing often mirrors Google campaigns. If you add negatives to Google, check if the same terms are wasting spend on Bing.
- **Broad match keywords:** Be extra cautious — broad match triggers many irrelevant searches. Consider shifting high-spend broad match keywords to phrase or exact match.
