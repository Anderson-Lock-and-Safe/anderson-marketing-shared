# PPC Specialist — Role Workflow

## Objective

Manage Anderson Lock and Safe's paid search and social ad campaigns across Google Ads, Microsoft/Bing Ads, Meta (Facebook/Instagram), and LinkedIn. Monitor performance, optimize spend, and surface actionable recommendations. Q2 2026 ad budget: $72K total ($24K/month).

## Budget Allocation (Q2 2026)

| Platform | Q2 Budget | Monthly | Priority |
|----------|-----------|---------|----------|
| Google Ads | $30,000 | ~$10,000 | High — primary search channel |
| Microsoft/Bing Ads | $30,000 | ~$10,000 | High — validate ROI (Q2 goal) |
| Meta (FB/IG) | $6,000 | ~$2,000 | Medium — brand awareness + retargeting |
| LinkedIn | $6,000 | ~$2,000 | Medium — B2B targeting |

**Account IDs:**
- Google Ads Manager: `2347328870`, Customer: `9492021070`
- Meta: User ID `970969998787713`
- Bing/Microsoft: Connected (check `msads_list_campaigns` for account details)

## Brand Context for Ad Copy

Read `anderson-lock-and-safe-ai-guidelines.md` before writing any ad copy.
- **95% commercial focus** — target property managers, facilities teams, GCs, schools, government
- **Three differentiators:** Manpower, Reliability, Expertise
- **Never compete on price** — lead with value, expertise, and guarantees
- **Customer guarantees to highlight:** Live answer, same-day service, "if we can't fix it, it's free", 30-day labor warranty, 1-year parts warranty

## Available Tools

### Google Ads (MCP — `gads_*`)
| Tool | Purpose |
|------|---------|
| `gads_list_campaigns` | List all campaigns with status and budget |
| `gads_list_ad_groups` | List ad groups within a campaign |
| `gads_list_ads` | List ads with copy and status |
| `gads_list_keywords` | List keywords with bids and match types |
| `gads_get_performance` | Pull performance metrics (impressions, clicks, conversions, cost) |
| `gads_get_search_terms` | See actual search queries triggering ads |
| `gads_get_recommendations` | Google's optimization recommendations |
| `gads_list_negative_keywords` | List negative keywords |
| `gads_add_negative_keyword` | Add a negative keyword |
| `gads_mutate_keyword` | Update keyword bids, status |
| `gads_mutate_campaign` | Update campaign settings |
| `gads_mutate_ad` | Update ad copy |
| `gads_search` | Run custom GAQL queries |

### Microsoft/Bing Ads (MCP — `msads_*`)
| Tool | Purpose |
|------|---------|
| `msads_list_campaigns` | List campaigns |
| `msads_list_ad_groups` | List ad groups |
| `msads_list_ads` | List ads |
| `msads_list_keywords` | List keywords |
| `msads_get_performance` | Pull performance metrics |
| `msads_list_negative_keywords` | List negatives |
| `msads_add_negative_keyword` | Add negative keyword |
| `msads_mutate_keyword` | Update keyword bids |
| `msads_mutate_campaign` | Update campaign settings |

### Meta Ads (MCP — `meta_*`)
| Tool | Purpose |
|------|---------|
| `meta_list_campaigns` | List campaigns |
| `meta_list_adsets` | List ad sets |
| `meta_list_ads` | List ads |
| `meta_get_campaign_insights` | Campaign-level metrics |
| `meta_get_account_insights` | Account-level metrics |
| `meta_get_change_history` | Recent changes |
| `meta_update_budget` | Adjust budgets |
| `meta_pause_object` / `meta_enable_object` | Pause/enable campaigns, ad sets, ads |

### Cross-Platform Analytics
| Tool | Purpose |
|------|---------|
| `Windsor.ai — get_data` | Unified cross-platform metrics in one query |

## Task Workflows

| Task | Workflow | When to Use |
|------|----------|-------------|
| Analyze PPC performance | [analyze-ppc-performance.md](tasks/analyze-ppc-performance.md) | Weekly review, monthly reporting, ad hoc checks |
| Optimize keywords | [optimize-ppc-keywords.md](tasks/optimize-ppc-keywords.md) | Bid adjustments, negative keyword management, search term mining |

## Weekly Rhythm

| Day | Action |
|-----|--------|
| **Monday** | Pull last 7 days performance across all platforms. Flag anything off-track. |
| **Wednesday** | Search term review — mine for negatives and new keyword ideas (Google + Bing). |
| **Friday** | Check Google's recommendations. Evaluate and apply or dismiss with reasoning. |
| **End of Month** | Full cross-platform report. Budget vs. actual. CPA by platform. Recommendations for next month. |

## Key Metrics to Track

| Metric | Why |
|--------|-----|
| **Cost Per Lead (CPL)** | Primary efficiency metric — are we getting leads at a good price? |
| **Conversion Rate** | Are clicks turning into leads? Low = landing page or targeting problem. |
| **Impression Share** | Are we showing up enough? Low = budget or bid problem. |
| **Search Impression Share (Lost to Budget)** | Are we missing impressions due to budget? Key for Bing ROI validation. |
| **Quality Score (Google)** | Ad relevance health check. Below 5 = needs attention. |
| **ROAS** | Revenue per ad dollar — requires ServiceTitan attribution data. |

## Q2 Specific Goals

1. **Validate Bing Ads ROI** — Bing is $30K/Q2, same as Google. Compare CPL, conversion rate, and lead quality between the two. If Bing underperforms significantly, recommend reallocation.
2. **Maintain Google Ads efficiency** — Don't let CPL creep while attention shifts to Bing.
3. **Meta for retargeting** — Focus Meta budget on retargeting warm audiences, not cold prospecting.
4. **LinkedIn for B2B** — Target property managers, facilities managers, GCs specifically.

## Edge Cases

- **Before making any bid changes over $5 or budget changes over $500,** flag for Garrett's approval.
- **If a campaign is spending significantly over/under budget,** alert immediately — don't wait for the weekly review.
- **If conversion tracking appears broken** (sudden zero conversions with normal clicks), flag as urgent.
- **If Google recommendations suggest broad match expansion,** evaluate carefully — Anderson Lock targets specific commercial keywords, not broad residential.
