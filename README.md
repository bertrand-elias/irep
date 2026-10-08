# irep: Interactive Review & Evidence Pipeline

Python CLI for evidence-verified document review: SHA-256 integrity checks, citation validation, LLM-drafted findings and a durable human approval loop.

> Supports a human reviewer; makes no approval, disposition, or governance decisions.

## Status

Early development, Stage 0 of 9 (scaffolding). Not functional yet.

## Why

Using an AI model to draft review findings accelerates analysis, but LLM output is untrustworthy when unconstrained. `irep` places deterministic integrity checks before the model and a durable human sign-off loop after it. This design is designed to ensure that every recorded finding is tied to verifiable evidence and remains under human judgment.

## How it works

1. **Verify package** *(planned)*: Run SHA-256 cryptographic checksums against `MANIFEST.sha256` to ensure artifact integrity.
2. **Check citations** *(planned)*: Validate deterministically that cited repository files, paths, and line references exist.
3. **Draft findings** *(planned)*: Analyze evidence and generate structured finding drafts using bounded LLM prompting.
4. **Human review** *(planned)*: Interactive CLI loop allowing the reviewer to inspect, accept, or reject each finding.
5. **Revise** *(planned)*: Refine and re-draft flagged findings based on explicit reviewer feedback.
6. **Export** *(planned)*: Compile the approved findings into a standardized, audit-ready markdown return document.

## Getting started

```bash
# Clone the repository
git clone <repo-url>
cd irep

# Install dependencies and sync virtual environment
uv sync

# Verify CLI entrypoint
uv run irep --version

# Run test suite
uv run pytest

```

## Design decisions

Key architectural choices and trade-offs are documented in [docs/decisions/](docs/decisions/), and brief requirements are tracked in [docs/requirements.md](docs/requirements.md).

## Licensing

Copyright (C) 2026 NatifDev.

Available under the GNU Affero General Public License v3.0 (`AGPL-3.0-only`); see `LICENSE`.
Commercial licenses are available from NatifDev.
