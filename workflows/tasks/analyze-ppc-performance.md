# Analyze PPC Performance — Task Workflow

## Objective

Pull performance data from all active ad platforms, normalize into a unified view, and surface actionable insights and recommendations.

## Required Inputs

| Input | Source | Example |
|-------|--------|---------|
| **Time period** | User request or default to last 7 days | `last 7 days`, `April 2026`, `last 30 days` |
| **Scope** | All platforms or specific | `all`, `google only`, `google vs bing comparison` |

## Steps

### 1. Pull Data from Each Platform

**Google Ads:**
```
Tool: gads_get_performance
Params: date_range (e.g., "LAST_7_DAYS" or custom start/end dates)
```
Key metrics: impressions, clicks, cost, conversions, conversion_value, CTR, CPC, conversion_rate

**Microsoft/Bing Ads:**
```
Tool: msads_get_performance
Params: date range
```
Key metrics: impressions, clicks, spend, conversions, CTR, CPC, conversion_rate

**Meta Ads:**
```
Tool: meta_get_account_insights
Params: date range
```
Key metrics: impressions, clicks, spend, actions (leads), CTR, CPC, CPM

**LinkedIn (if data accessible via Meta or Windsor.ai):**
Check Windsor.ai `get_data` with LinkedIn connector if available.

### 2. Normalize the Data

Create a unified comparison table. Note platform-specific naming differences:
- Google "cost" = Bing "spend" = Meta "spend"
- Google "conversions" ≈ Bing "conversions" ≈ Meta "actions" (filter to lead-type actions)
- Currency: all USD, but Google Ads reports cost in micros (divide by 1,000,000), Meta in cents (divide by 100)

### 3. Generate the Cross-Platform Summary

```
## PPC Performance Report — [Time Period]

### Cross-Platform Summary

| Platform | Impressions | Clicks | CTR | Cost | Conversions | CPL | Conv Rate |
|----------|------------|--------|-----|------|-------------|-----|-----------|
| Google   | ...        | ...    | ... | ...  | ...         | ... | ...       |
| Bing     | ...        | ...    | ... | ...  | ...         | ... | ...       |
| Meta     | ...        | ...    | ... | ...  | ...         | ... | ...       |
| LinkedIn | ...        | ...    | ... | ...  | ...         | ... | ...       |
| **Total**| ...        | ...    | ... | ...  | ...         | ... | ...       |

### Budget Tracking

| Platform | Monthly Budget | Spent MTD | % Used | Pace (on/over/under) |
|----------|---------------|-----------|--------|---------------------|
| Google   | $10,000       | ...       | ...    | ...                 |
| Bing     | $10,000       | ...       | ...    | ...                 |
| Meta     | $2,000        | ...       | ...    | ...                 |
| LinkedIn | $2,000        | ...       | ...    | ...                 |

### Platform-Specific Insights

**Google Ads:**
- Top campaign: [name] — [performance summary]
- Bottom campaign: [name] — [what's wrong]
- [1-2 specific observations]

**Bing Ads:**
- [Bing vs Google comparison — key for Q2 ROI validation goal]
- [1-2 specific observations]

**Meta:**
- [Retargeting vs prospecting performance if distinguishable]
- [1-2 specific observations]

### Recommendations
1. [Specific, actionable, includes dollar impact if possible]
2. [Specific, actionable]
3. [Specific, actionable]

### Alerts (if any)
- ⚠️ [Anything needing immediate attention]
```

### 4. Deliver Report

- **Weekly check:** Output directly to user
- **Monthly report:** Create as ClickUp task in PERFORMANCE > Weekly PPC Digests
- **Alert:** If anything is urgent, also send to Google Chat (Claude Code Remote space)

## Edge Cases

- **Conversion data delayed:** Google and Bing conversions can lag 1-3 days. Note this if looking at very recent data. "Last 7 days may undercount conversions by 10-20% due to attribution delay."
- **Platform API returns errors:** Note which platform failed and report what you can from the others. Don't block the whole report because one API is down.
- **Zero conversions:** Check if conversion tracking is working (look at click volume — if clicks are normal but conversions are zero, tracking may be broken).
- **Currency/unit confusion:** Always verify units. Google cost = micros, Meta spend = sometimes cents. When in doubt, cross-check against the platform dashboard.
