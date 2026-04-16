# Tools Index

Python scripts and shell utilities for deterministic execution. These exist because CLI tools or MCP tools can't handle the specific operation (batch operations, multi-step orchestration, data transforms).

**Tool hierarchy:** CLI → MCP → Custom script. Only build here when the first two can't do it.

## Current Tools

| Tool | Type | Purpose | Status |
|------|------|---------|--------|
| `buffer_publish.py` | Python | Publish/schedule/draft social posts via Buffer GraphQL API | ✅ Working |
| `send_gchat.sh` | Shell | Send a message to Google Chat via the bot service account | ✅ Working |

## Planned Tools

| Tool | Purpose | Phase |
|------|---------|-------|
| `bulk_clickup_tasks.py` | Create 30+ ClickUp tasks from a content kit | Phase 2 |
| `content_kit_generator.py` | Orchestrate full content kit generation + ClickUp population | Phase 5 |
| `performance_aggregator.py` | Pull metrics from multiple ad platforms into one view | Phase 4 |
| `calendar_to_buffer.py` | Parse engagement calendar markdown → Buffer API calls | Phase 1 (if needed) |

## Dependencies

Scripts should be zero-dependency where possible (using only Python stdlib + `httpx` or `requests` for HTTP).

If a script needs packages, add them to `requirements.txt` in this directory.

## Environment Variables

Scripts that need API keys read from `.env` in the project root (gitignored). See `.env.example` for required variables.

## Conventions

- All scripts should be runnable standalone: `python tools/script.py --help`
- All scripts should handle errors gracefully and output clear error messages
- Scripts that call paid APIs should have a `--dry-run` flag
- Log what you're doing so the agent (Claude) can understand what happened
