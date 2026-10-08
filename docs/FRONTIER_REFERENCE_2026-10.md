# AEON Frontier Reference Bars — 2026-10

These are **reference bars**, not direct AEON comparisons. Vendor-reported scores can use different effort settings, safeguards, tools, prompts, and harnesses.

## OpenAI — GPT-6 Astra

Official OpenAI reporting:

- GPQA Diamond: **96.0%**
- Terminal-Bench 4.0: **57.9%**
- DeepSWE v1.1: **74.1%**
- FrontierCode 1.1 Main: **53.3%**
- FrontierCode 1.1 Extended: **64.5%**
- FrontierMath Tier 4 v2: **97.6%**
- Humanity's Last Exam with tools: **57.2%**

OpenAI describes Astra as its highest-capability GPT-6 model and reports state-of-the-art performance across computer use, browsing, software engineering, science, and professional work.

## Anthropic — Claude Opus 5.5

Anthropic's September 2026 launch table reports:

- Terminal-Bench 4.0: **66.4%** at xhigh
- FrontierCode v1.1 Main: **54.4%**
- CursorBench 4.0: **57.8%**
- GDPval-AA v2.1: **1846 Elo**
- AutomationBench: **40.0%**
- Humanity's Last Exam with tools: **67.7%**
- Terminal-Bench-Science 0.1: **58.7%**
- OSWorld 2.0 partial: **81.8%**
- Chartography with tools: **89.0%**

Anthropic notes that Opus 5.5 normally uses adaptive thinking at max effort, Terminal-Bench uses xhigh, production safeguards were enabled, and some safeguard interventions route work to other Claude models. Those conditions must be preserved when interpreting the numbers.

## OpenAI — GPT-6.1 Sol

Official OpenAI materials describe GPT-6.1 Sol as near-Astra performance at lower cost. The published GPT-6 Sol family comparisons include:

- AutomationBench: GPT-6 Sol xhigh **33.2%** at **$0.27/task**
- Agents' Last Exam: **56.4%** at max effort in the published comparison
- DeepSWE v1.1: **68.8%** at max effort
- OSWorld 2.0 offline: **60.5%** at xhigh

GPT-6.1 Sol has a 1.05M context window and supports reasoning effort through max according to the current API model documentation.

## Direct-comparison policy

AEON must not claim parity or superiority from these numbers alone.

For a publishable direct comparison:

1. Freeze the benchmark version.
2. Use identical test items.
3. Use identical scoring.
4. Match or explicitly report tool access.
5. Match or explicitly report reasoning/effort budgets.
6. Do not allow hidden fallback models for AEON.
7. Record all retries and failures.
8. Record token/compute/tool cost.
9. Record wall-clock latency.
10. Use paired statistical analysis.
11. Report the full quality-vs-cost frontier, not only the best point.

## AEON target

The ambitious research target is **not universal benchmark domination**.

The first decisive success criterion is:

> On at least one frontier-relevant workload, AEON must match or exceed a strong frontier-quality baseline while using materially less measured compute/cost, without test leakage, privileged oracle information, precomputation of unchosen branches, or hidden fallback models.

A stronger architecture claim requires this result to replicate across independent capability families.
