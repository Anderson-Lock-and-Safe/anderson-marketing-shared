# Pull ServiceTitan Data — Task Workflow

## Objective

Extract revenue, job, and customer data from ServiceTitan to inform marketing strategy, campaign targeting, and performance attribution.

## Required Inputs

| Input | Source | Example |
|-------|--------|---------|
| **Data type** | User request | "revenue by job type", "customer list", "new vs repeat" |
| **Time period** | User request or default 90 days | `last 90 days`, `Q1 2026`, `YTD` |

## Available Tools

| Priority | Tool | Purpose |
|----------|------|---------|
| 1 (MCP) | **ServiceTitan** — `st_api` | Call any ServiceTitan REST API endpoint |
| 1 (MCP) | **ServiceTitan** — `st_schema` | Explore available API endpoints and schemas |
| 1 (MCP) | **ServiceTitan** — `st_auth_check` | Verify connection is active |

**Tenant ID:** `1384623141`

## Steps

### 1. Verify Connection

Call `st_auth_check` to confirm the ServiceTitan connection is active.

### 2. Explore Available Data

Call `st_schema` to understand available endpoints. Common ones:

| Endpoint | Data |
|----------|------|
| Jobs | Job details, type, status, revenue, dates |
| Customers | Customer info, tags, address, contact |
| Invoices | Revenue details, line items |
| Estimates | Quotes, conversion tracking |
| Memberships | Recurring service agreements |

### 3. Pull the Requested Data

Use `st_api` with appropriate endpoint, filters, and date ranges.

### 4. Summarize for Marketing Use

Transform raw data into actionable marketing insights:

```
## ServiceTitan Data Pull — [Date]

### Revenue by Job Type (Last 90 Days)

| Job Type | Jobs | Revenue | Avg Revenue/Job | % of Total |
|----------|------|---------|----------------|-----------|
| Access Control | ... | ... | ... | ... |
| Commercial Rekey | ... | ... | ... | ... |
| Safe Service | ... | ... | ... | ... |
| ... | ... | ... | ... | ... |

### Customer Segments

| Segment | Count | Revenue | Avg Lifetime Value |
|---------|-------|---------|-------------------|
| Property Management | ... | ... | ... |
| General Contractors | ... | ... | ... |
| Schools/Education | ... | ... | ... |
| ... | ... | ... | ... |

### New vs. Repeat Customers

| Type | Count | Revenue | % of Total Revenue |
|------|-------|---------|-------------------|
| New | ... | ... | ... |
| Repeat | ... | ... | ... |

### Marketing Implications
1. [Insight that should inform campaign targeting]
2. [Insight about growing/declining service areas]
3. [Insight about customer retention]
```

### 5. Deliver

- Output directly if on-demand
- Save to ClickUp (PERFORMANCE > Attribution Tracking) if part of monthly cycle
- Feed into brainstorm prep if timed for monthly session

## Edge Cases

- **If ServiceTitan API returns paginated results,** follow pagination to get complete data. Don't report on partial data without noting it.
- **If certain fields are empty or null,** note which data is incomplete. ServiceTitan data quality varies by how consistently the team enters info.
- **If the connection fails,** flag for Garrett. ServiceTitan auth may need renewal. Document what data was needed so it can be pulled manually.
- **Revenue data may not include all line items.** Cross-reference with invoices if total revenue seems low.
