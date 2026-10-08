# AEON Frontier Evaluation Matrix

Status: research infrastructure; **not a claim of frontier parity**.

## Goal
Evaluate AEON on the same broad capability dimensions used by current frontier systems, while separating:

1. direct same-harness measurements;
2. vendor-reported reference scores;
3. third-party leaderboard measurements;
4. unavailable/not-comparable measurements.

AEON must never be declared better from a vendor-reported score unless AEON was evaluated on the same benchmark release, prompt/tool policy, effort budget, and scoring harness.

## Frontier reference models

- OpenAI GPT-6 Astra — flagship/highest-capability reference.
- OpenAI GPT-6.1 Sol — near-Astra lower-cost reference.
- Anthropic Claude Opus 5.5 — current Opus flagship reference.
- Additional references when useful: Gemini flagship, open-weight frontier models, Claude Fable where benchmark data exists.

## Benchmark families

| Capability | Primary benchmark(s) | Secondary | AEON status | Required comparison |
|---|---|---|---|---|
| General knowledge | MMLU / MMLU-Pro | SimpleQA | harness to implement | same dataset + prompt protocol |
| Scientific reasoning | GPQA-Diamond | HLE | harness to implement | exact benchmark release |
| Abstract reasoning | ARC-AGI-2 | BBH | harness to implement | exact scoring |
| Mathematics | AIME 2025/2026, MATH-500 | FrontierMath | harness to implement | contamination/knowledge cutoff recorded |
| Coding | LiveCodeBench | HumanEval/MBPP+ | harness to implement | executable tests |
| Software engineering | SWE-bench Verified/Pro | DeepSWE / FrontierCode | adapter design | isolated repo + fixed harness |
| Terminal agents | Terminal-Bench 4 | Terminal-Bench-Science | adapter design | sandbox + action accounting |
| Computer use | OSWorld 2.0 | BrowseComp | adapter design | identical environment |
| Professional agents | Agents' Last Exam | AutomationBench | adapter design | tool/action/cost accounting |
| Multimodal reasoning | MMMU | multimodal task suite | adapter design | exact image inputs |
| Long-context/memory | custom held-out memory suite | long-context public suites | runnable locally | persistent-state + retrieval accounting |
| Adaptive computation | custom AEON suite | adaptive-depth baselines | runnable locally | quality-vs-compute frontier |
| Resource efficiency | cost/latency/token metrics | energy/memory | runnable locally | real execution, not proxy-only |

## Current frontier references from official/public sources

OpenAI reports GPT-6 Astra as state-of-the-art across computer use, browsing, software engineering, cybersecurity, science, and professional work. OpenAI reports GPT-6.1 Sol as near-Astra performance at lower cost and publishes direct comparisons on AutomationBench, Agents' Last Exam, FrontierCode, DeepSWE, and OSWorld. See the cited sources in the research report.

Anthropic reports Claude Opus 5.5 as its strongest Opus model and publishes benchmark comparisons including Terminal-Bench 4.0 and other agentic evaluations. Production safeguards and fallback behavior must be recorded when comparing.

## Direct-comparison rule

For every benchmark where frontier API access is available:

- freeze benchmark version;
- freeze prompts/system instructions;
- freeze tool availability;
- freeze reasoning/effort policy;
- run AEON and frontier systems on the same items where licensing permits;
- blind scoring where possible;
- record wall-clock and monetary cost;
- record failures, retries, tool calls, and tokens;
- use paired bootstrap confidence intervals;
- report both quality and quality/cost Pareto frontier.

## Important non-comparability rule

Vendor-reported scores are **reference bars**, not direct AEON comparisons. Different model prompts, hidden scaffolding, tool access, effort settings, fallback models, and benchmark versions can materially change results.

## AEON target

The research target is not “beat every frontier model on every benchmark.” The stronger scientific target is:

> Demonstrate that AEON's persistent typed computational substrate produces a statistically significant quality/compute or capability/cost advantage on at least one difficult frontier-relevant workload while maintaining parity or improvement on other capability families, under matched evaluation conditions.

A broad superiority claim requires repeated wins across independent capability families and strong baselines.
