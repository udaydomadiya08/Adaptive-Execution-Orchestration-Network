# AEON — Scientific Final Disposition

## Status
RESEARCH PROGRAM COMPLETE — RELEASE CLAIMS FROZEN

This document is the final scientific disposition of the AEON research program. It deliberately distinguishes engineering completion from scientific proof and preserves negative, blocked, and invalidated evidence.

## 1. Core question

AEON investigated whether a persistent computational state can dynamically compose heterogeneous computational mechanisms and allocate computation adaptively, potentially improving the quality–compute frontier relative to fixed or static heterogeneous systems.

The strongest version of the hypothesis was:

> A target-free controller operating on persistent computational state can learn when to invoke heterogeneous operators, in what sequence, and when to stop, using ordinary task supervision and without privileged counterfactual labels, while improving quality–compute–latency tradeoffs against matched fixed baselines.

## 2. What is established

### Established with substantial evidence

1. Heterogeneous operators/specialists can have complementary capabilities.
2. Persistent computational state can preserve useful information across transitions.
3. Input-dependent routing can outperform fixed specialists on some controlled and real-data mixtures.
4. Counterfactual policy-value supervision can sometimes produce selective computation with useful quality–proxy-cost tradeoffs.
5. Strict no-test-label/no-precompute accounting is feasible and materially changes which historical results remain valid.
6. Controller overhead can erase proxy-compute savings in real wall-clock measurements.
7. Distribution shift can substantially weaken learned routing.
8. Reward-only adaptive sequencing can learn nontrivial policies in some controlled settings, but the effect is inconsistent and not a reliable compute-efficiency improvement.

## 3. Final intrinsic-policy experiment

A fresh reward-only policy-gradient experiment was created specifically to test the unresolved AEON hypothesis.

Protocol:
- 12-dimensional synthetic inputs.
- Hidden regimes were not exposed to the controller.
- Three heterogeneous recurrent state transitions.
- Up to three sequential actions.
- Explicit STOP action.
- Controller observed persistent state, uncertainty statistics, time, and used-operator mask.
- Training signal was terminal task correctness minus a compute-cost penalty.
- No counterfactual specialist labels were provided.
- Test-time specialist outputs were not precomputed for routing.
- Five independent seeds: 7, 17, 27, 37, 47.
- Fixed-policy comparator was selected on training data only and then frozen for test evaluation.

Final means:

| Metric | Reward-only adaptive | Training-selected fixed |
|---|---:|---:|
| Test accuracy | 53.96% | 51.24% |
| Proxy cost | 2.69 | 2.60 |
| Mean adaptive steps | 1.42 | fixed |

The adaptive policy was positive on 4/5 seeds, but its mean proxy cost was slightly higher than the selected fixed comparator. Therefore this experiment is **not evidence of a quality–compute improvement**. A privileged per-instance sequence oracle reached 74.44% mean accuracy at 2.76 mean proxy cost, demonstrating remaining headroom but not deployable performance.

The result closes, rather than proves, the claim that ordinary terminal reward is sufficient for the current intrinsic controller architecture.

## 4. Major surviving evidence

### Policy-level value supervision
AEON-1.65 remains the strongest controlled policy-value result: 71.24% versus 64.18% best fixed on a fresh heterogeneous synthetic task, with approximately 22.5% lower proxy cost than exhaustive execution. This is diagnostic/promising evidence, not universal proof.

### Real-data transfer
Clean real-data experiments include positive/negative results on digits, diabetes, breast cancer, Fair, RANDHIE, and ANES96. The corrected Fair experiment remained positive after leakage correction, while several earlier apparently strong real-data results were invalidated because STOP decisions used target information.

### Persistent computation
AEON-1.79/1.81 established that persistent state can improve a second computation over a reset control on controlled complementary tasks. The controller did not reliably learn when to invoke that refinement.

## 5. Closed or rejected directions

The following were tested and should not be reopened without a genuinely new hypothesis:

- naive adaptive halting
- scalar marginal-computation value
- post-hoc thresholding as a substitute for learned control
- generic cheap probes
- pairwise specialist-value prediction
- outcome prediction as a universal routing solution
- hand-designed memory affordance routing
- learned memory affordance transfer
- naive invariant learned representations
- hierarchical routing without demonstrated benefit
- arbitrary sequential composition without state-contract guarantees
- separate post-hoc controller on persistent state
- reward-only intrinsic controller as currently formulated

Repeated capacity/threshold/augmentation tweaks are not justified by the existing evidence.

## 6. Integrity conclusions

The research program explicitly invalidated experiments with:
- test-label STOP leakage;
- precomputed unchosen specialist outputs used for adaptive decisions;
- hard-coded expert accuracies;
- synthetic noise substituted for real operator execution;
- privileged oracle information presented as deployable controller behavior.

Those results remain archived but must not be used as positive evidence.

## 7. Prior-art / novelty boundary

AEON must not claim novelty merely for:
- adaptive computation;
- early exit/halting;
- heterogeneous experts;
- dynamic routing;
- recurrent computation;
- memory-augmented computation;
- Transformer/SSM hybrids.

These areas already contain substantial prior work. AutoMoE, for example, explicitly studies heterogeneous experts with adaptive computation. Recent 2026 work studies constrained adaptive test-time compute allocation, end-to-end resource-adaptive inference, and dynamic compute allocation in recurrent Transformers.

The potentially distinctive AEON research question is the combination of persistent state, heterogeneous transitions, and learned sequential control under strict no-leakage accounting. The present evidence does not establish that combination as a universally superior new paradigm.

## 8. Final scientific claim

The strongest defensible claim is:

> AEON is a reproducible reference architecture for heterogeneous adaptive computation with persistent state. Experiments show that heterogeneous capabilities can be selectively allocated and that policy-value supervision can sometimes improve quality–proxy-compute tradeoffs. However, reliable target-free intrinsic learning of multi-step heterogeneous computation remains task-dependent and is not demonstrated as a universal advantage.

## 9. What cannot be claimed

AEON has NOT scientifically proved:

- universal superiority over Transformers or modern LLMs;
- universal compute or latency savings;
- a new fundamental computational primitive;
- a generally optimal learned controller;
- generalization of adaptive policies to arbitrary unseen workloads;
- a theorem that heterogeneous adaptive computation is universally better.

## 10. Stopping decision

The research program is considered scientifically complete because:

1. the core hypothesis was made falsifiable;
2. multiple controller formulations were tested;
3. positive and negative controls were run;
4. independent real-data tasks were evaluated;
5. distribution-shift tests were performed;
6. wall-clock and proxy-cost discrepancies were measured;
7. leakage and invalidation audits were performed;
8. modern prior art was checked;
9. the remaining strongest hypothesis was directly tested with reward-only control;
10. that test did not establish a universal compute-efficiency advantage;
11. further small controller tweaks would constitute result-seeking rather than principled research.

Therefore the project should now move from research mode to publication/release mode, with the bounded claim above.
