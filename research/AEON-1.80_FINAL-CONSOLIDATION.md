# AEON-1.80 — Final Research Consolidation / Phase Closure

## Purpose
This document freezes the evidence accumulated through AEON-1.79 and closes the current adaptive-routing/policy-value research phase. It is intentionally conservative: invalidated experiments are retained as historical records but excluded from scientific support.

## 1. Core question
Can a controller dynamically choose heterogeneous computation, including whether to continue or stop, in a way that improves the quality–computation tradeoff?

## 2. Evidence-integrity rule
A result is usable only if:
- test labels are unavailable to routing/stopping;
- unselected test operators are not precomputed;
- controller supervision is derived only from development/controller data;
- fixed baselines are trained/evaluated under the same data protocol;
- proxy cost and wall-clock claims are not conflated;
- failed/blocked experiments remain visible.

## 3. Evidence status

### Strongest valid positive evidence
**AEON-1.65 — synthetic policy-level cost-to-go**
- 5 seeds.
- AEON 71.24% vs best fixed 64.18%.
- +7.07 pp; positive on all five seeds.
- Policy-level value target outperformed immediate-marginal formulations tested earlier.
- Synthetic; privileged controller-split counterfactual supervision; proxy cost.

**AEON-1.66 — digits transfer**
- AEON 97.69% vs best fixed 97.42%.
- Positive/non-inferior across five seeds, but only ~1.51 pp oracle headroom.
- Useful as transfer evidence, not a strong adaptive-computation proof.

**AEON-1.67 — real Diabetes regression**
- AEON 43.1605 MAE vs best fixed 43.7073.
- ~1.25% lower MAE.
- Cost-matched fixed comparison favored AEON on all five seeds.
- Target-free stop baseline documented.
- Small dataset; controller remains biased toward cheap first computation.

**AEON-1.75 corrected Fair regression**
- 6,366 real observations.
- Corrected target-free STOP decision.
- AEON 0.948558 MAE vs best fixed 0.983697.
- 3.57% lower MAE, positive on all five seeds.
- Mean proxy cost 0.639196; ~0.484673 specialist executions/sample.
- This is the strongest clean real-data result in the current phase.

### Negative / boundary evidence
- 1.04/0.4-era marginal-value and learned halting approaches: weak credit assignment.
- 1.15–1.20 adaptive-compute/latency/value controllers: no robust efficiency solution.
- 1.22 shared latent contract: heterogeneous composability failure.
- 1.29 candidate-output routing: precompute leakage; not valid efficiency evidence.
- 1.32–1.34 sequential/counterfactual controllers: small or negative gains; cost/quality tradeoff unstable.
- 1.36 cheap probe: promising on one mixed capability benchmark but not universal.
- 1.37 hierarchy: no meaningful benefit over flat routing.
- 1.45 memory-affordance transfer: failed under shifted formats.
- 1.48 learned invariant representation: collapsed; branch closed.
- 1.51 digits input-only routing: no wall-clock gain; branch closed.
- 1.53–1.54 entangled/shifted digits competence routing: negative.
- 1.56 static cheap diagnostic: negative.
- 1.57 outcome-prediction diagnostic: modest, not superior to fixed baseline.
- 1.58–1.60 cross-task outcome/pairwise/cheap-probe variants: no general solution.
- 1.61 probe-as-gate: negative/unstable.
- 1.62–1.64 value-of-information / partial execution / immediate marginal control: negative or boundary.
- 1.69 natural breast-cancer complementarity: controller executed all specialists; no adaptive savings.
- 1.72 realized-outcome weak supervision: failed.
- 1.73 uncertainty-aware offline/realized-outcome learning: failed.
- 1.75 corrected Diabetes, RANDHIE, ANES96: negative.
- 1.76 real wall-clock digits: controller overhead dominated; adaptive route slower than fixed specialists.
- 1.77 coarse routing: amortized controller cost but increasingly behaved like fixed routing and did not establish speed advantage.
- 1.78 expensive independent specialists: adaptive black-box routing remained slower than fixed specialists.
- 1.79 persistent-state adaptive controller: fixed state-conditioned refinement contained useful information, but learned controller failed to discover/use it.

### Invalidated evidence
The following later runs directly used the held-out test target in STOP/CONTINUE logic and therefore cannot support adaptive-computation claims:
- 1.68
- 1.70
- 1.71
- 1.74

Their artifacts remain preserved for audit history. They are excluded from all conclusions.

## 4. What AEON has actually demonstrated
The defensible claim is narrow:

> Counterfactual policy-value supervision can sometimes learn selective computation policies that improve task quality at lower nominal computation cost on controlled and at least one clean real-data task, but the effect is strongly task-dependent and does not yet generalize reliably across real datasets or produce demonstrated wall-clock/energy savings.

This is evidence for a **conditional computational-control mechanism**, not evidence that AEON is a general replacement for transformers, modern language models, or existing AI systems.

## 5. What has NOT been demonstrated
- General adaptive-computation superiority.
- Real hardware speedup.
- Energy savings.
- Generalization across modalities.
- Task-agnostic controller transfer.
- Learning useful policy value purely from ordinary online execution feedback.
- Broad three-way or many-way specialist routing.
- Persistent-state adaptive computation superiority.
- Superiority to modern LLM architectures.

## 6. Architectural conclusion
The experiments strongly disfavor the architecture:

`input -> controller -> choose black-box specialist -> execute specialist`

because controller overhead and independent specialist execution erase the expected runtime advantage.

The experiments also show that merely adding a persistent-state wrapper is insufficient. The state-conditioned computation itself can contain useful information, but credit assignment for deciding when to use it remains unresolved.

The next credible AEON architecture should therefore make **computation sharing intrinsic to the state transition**, rather than treating operators as independent black boxes. Any future controller must be evaluated with real execution accounting from the beginning.

## 7. Branch decisions
### CLOSED
- static-feature competence routing;
- naive environment classification routing;
- pairwise immediate value;
- greedy immediate marginal correctness;
- weak realized-outcome supervision;
- uncertainty-only rescue of weak supervision;
- black-box runtime routing;
- coarse-granularity routing as a complete solution;
- persistent-state controller in its current formulation.

### RETAIN AS CORE HYPOTHESIS
- policy-level cost-to-go / continuation value under counterfactual training supervision;
- computation as reusable state transitions rather than independent specialist calls.

## 8. Phase-completion decision
**STATUS: PHASE COMPLETE — CONDITIONAL MECHANISM ESTABLISHED, GENERAL SYSTEM NOT ESTABLISHED.**

This phase has reached a scientifically useful stopping point. Further work should begin as a new architectural phase, not as a continuation of tiny benchmark iterations.

## 9. Reproducibility principle
Future AEON experiments must fail closed if any test target enters routing, stopping, policy selection, normalization, threshold selection, or adaptive cost accounting. A future runner should include an explicit leakage sentinel and log all information available to the controller at each test-time decision.
