# AEON-3 — Frontier Integration Research Contract

Status: **active research — not release**.

## Why AEON-3 exists

AEON's ultimate hypothesis cannot be evaluated fairly by comparing a small toy substrate against frontier general-purpose models. The next generation therefore separates:

- **foundation competence**: a strong pretrained model or specialist;
- **AEON substrate**: persistent state, memory, typed capabilities, planning, verification and resource control;
- **environment**: tools, files, browser, code execution or other information sources.

The scientific question becomes:

> Given the same underlying foundation competence, does AEON's persistent adaptive substrate produce better capability/cost/latency/reliability tradeoffs than the foundation model's native inference strategy or a strong external agent scaffold?

## Frontier integration modes

### Mode 1 — Sidecar controller

`frontier model -> AEON controller/memory -> frontier model`

Useful for determining whether AEON can improve an existing model without changing its weights.

### Mode 2 — Tool/skill orchestrator

`frontier model + typed specialists + memory + verifier + tools <- AEON planner`

Tests whether AEON can allocate different capabilities around a strong model.

### Mode 3 — State-integrated model

`foundation hidden state <-> persistent AEON state <-> adaptive transitions`

This is the most ambitious architecture and requires model-level integration.

## Required baselines

For every frontier-relevant benchmark:

1. Base frontier model, fixed effort.
2. Base frontier model, native adaptive/thinking mode where available.
3. Strong agent scaffold using the same tools.
4. AEON + same base model + same tools.
5. AEON + same base model + reduced resource budget.
6. Oracle adaptive policy only as a diagnostic ceiling.

## Required metrics

Quality:
- benchmark score;
- pass@k where applicable;
- task completion;
- verifier correctness;
- robustness under distribution shift.

Resources:
- input/output tokens;
- hidden/reasoning tokens when exposed;
- API dollars;
- tool calls;
- model invocations;
- wall-clock latency;
- peak memory;
- bandwidth;
- energy where measurable.

Reliability:
- retry count;
- timeout rate;
- invalid tool actions;
- unsafe/unauthorized actions;
- fallback usage;
- catastrophic failures.

## AEON success criteria

A strong AEON result requires a Pareto improvement, not a single benchmark win.

Minimum breakthrough evidence:

- same or better quality than the matched baseline;
- materially lower measured resource cost on a difficult workload;
- no hidden fallback model;
- no precomputation of unchosen branches;
- no test labels or oracle signals at inference;
- replication across at least three independent task families;
- statistical uncertainty reported;
- ablations show the gain comes from AEON's architecture rather than simply more model calls.

## Current frontier reference bars

See `FRONTIER_REFERENCE_2026-10.md`.

These are external reference bars only until the same benchmark/harness is run directly.

## Research priority

The highest-value next experiment is **AEON sidecar control around a strong foundation model** on a task where adaptive computation has a clear cost signal: coding agents, long-horizon tool tasks, or scientific workflows.

This is preferable to another synthetic classifier benchmark.
