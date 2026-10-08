# AEON — Final Research Consolidation

## Status
**RESEARCH PHASE COMPLETE — RELEASE DECISION PENDING USER INSTRUCTION**

This document closes the substantive research program. It does **not** claim that AEON universally outperforms modern architectures. It records what was actually established, what failed, what was invalidated, and where the remaining scientific uncertainty lies.

## 1. Core research question

Can a persistent computational substrate dynamically compose heterogeneous computation and allocate additional computation only when its expected value exceeds its resource cost?

The intended objective is a quality/resource Pareto improvement, with resource accounting separated into proxy compute and measured wall-clock/energy.

## 2. Prior-art audit

The general ingredients of AEON are established research areas:

- Adaptive Computation Time and recurrent halting predate AEON.
- PonderNet explicitly learns adaptive computation with a compute-quality objective.
- Universal Transformers combine recurrent state updates, attention, and adaptive halting.
- Sparse MoE systems already learn conditional expert routing.
- Mixture-of-Depths allocates computation dynamically under an explicit budget.
- LayerSkip demonstrates early exit and self-speculative execution with shared computation.
- Mixture-of-Recursions combines parameter sharing with token-level adaptive recursive depth.
- Recent 2025–2026 work such as Dr.LLM and BUDDY demonstrates learned dynamic layer routing and budget-conditioned inference.
- Hybrid Transformer/SSM architectures such as Jamba, Samba, and later systematic hybrid studies already combine heterogeneous sequence mechanisms.

Therefore AEON cannot claim novelty merely from “adaptive routing,” “adaptive halting,” “heterogeneous operators,” “persistent state,” or “Transformer + SSM hybridization.”

## 3. Evidence-integrity policy

A result is admissible only when:

1. test labels are inaccessible to routing/stopping;
2. unselected test operators are not precomputed;
3. policy supervision comes only from training/controller data;
4. fixed baselines use the same data protocol;
5. proxy compute is not presented as wall-clock speed;
6. blocked and failed experiments remain visible;
7. exact operator implementations are used when claims depend on them;
8. oracle policies are treated only as diagnostic ceilings.

## 4. Research evidence

### Positive evidence

**AEON-0.1:** controlled synthetic heterogeneous routing demonstrated that learned routing can outperform fixed/random operator mixtures under the constructed workload.

**AEON-1.3/1.4:** persistent/contextual episodic addressing showed strong memory behavior on controlled long-context tasks.

**AEON-1.13:** specialist capability separation was measurable across seven task families.

**AEON-1.52/1.55:** real-data domain-aware routing produced large gains when domain structure strongly predicted specialist competence. Audit showed that much of the effect was explainable by identifiable domain cues.

**AEON-1.65:** five-seed synthetic policy-level cost-to-go supervision produced 71.24% vs 64.18% best fixed, with positive improvement on all five seeds and lower nominal proxy cost than executing all specialists. This is the strongest controlled evidence for policy-level value supervision.

**AEON-1.66:** small real digits transfer was positive/non-inferior but had little oracle headroom.

**AEON-1.67:** target-free Diabetes policy control showed a small clean improvement over fixed baselines.

**AEON-1.75 corrected Fair:** 6,366 real observations; target-free stopping; 0.948558 MAE vs 0.983697 best fixed, positive on all five seeds. This is the strongest clean real-data selective-computation result in the historical program.

**AEON-1.79:** persistent state-conditioned refinement itself added information relative to resetting state, but the learned adaptive controller did not reliably learn when to invoke it.

## 5. Major negative findings

- Immediate marginal-value controllers failed or were unstable.
- Learned halting repeatedly collapsed or received poor credit assignment.
- Black-box specialist routing did not produce real wall-clock advantage; controller overhead often dominated.
- Coarse routing amortized overhead but increasingly became fixed routing.
- Static feature competence prediction did not generalize reliably under representation shift.
- Learned memory-affordance shortcuts failed under shifted formats.
- Learned invariant representations collapsed in one major branch.
- Weak realized-outcome supervision was insufficient.
- Uncertainty-only mechanisms did not solve adaptive control.
- Persistent state did not by itself solve controller credit assignment.
- Real-data policy gains were strongly task-dependent.

## 6. New Phase-3 intrinsic-control research

### 6.1 End-to-end intrinsic controller

A fresh state-only controller was trained end-to-end with straight-through Gumbel routing over three heterogeneous transitions and an explicit STOP action. No counterfactual policy labels were supplied.

With no compute penalty:
- mean adaptive accuracy: **62.56%**
- best fixed operator: **63.63%**
- oracle specialist accuracy: **83.15%**
- mean adaptive steps: **1.09**

With a small compute penalty (0.005):
- mean adaptive accuracy: **63.37%**
- best fixed operator: **63.44%**
- mean adaptive steps: **1.00**

Interpretation: the end-to-end intrinsic controller did not learn useful multi-step computation. It largely collapsed to one-step behavior despite substantial oracle headroom.

### 6.2 Static-mixture control

A learned global mixture over the same heterogeneous operators achieved approximately **63.44%** mean accuracy at expected cost ~2.11. The adaptive controller did not materially outperform this simpler control.

Interpretation: the observed small adaptive gains are not evidence that learned sequential control itself is the source of the benefit.

### 6.3 Policy-supervised persistent-state attempt

A fresh exact history-enumeration implementation was attempted to test whether privileged training-only cost-to-go supervision could rescue persistent-state adaptive control. The computation required by exact history enumeration exceeded practical CPU execution limits in this environment.

Status: **BLOCKED BY COMPUTATIONAL COST**, not counted as positive or negative scientific evidence. The historical AEON-1.65 policy-value result remains the valid evidence for this supervision strategy.

## 7. Invalidated experiments

AEON-1.68, 1.70, 1.71, and 1.74 used held-out targets in STOP/CONTINUE decisions and are excluded from scientific conclusions.

AEON-0.16's headline Mamba result was invalidated because the runner did not execute the claimed experts and instead used hard-coded expert outcomes/synthetic noise.

AEON-1.14's adaptive-computation interpretation was downgraded because routing features included all candidate expert predictions/confidences before selection.

## 8. Scientific conclusion

The strongest defensible conclusion is:

> **Heterogeneous adaptive computation is feasible and can produce task-dependent quality–nominal-compute improvements when useful competence differences are identifiable and the controller receives sufficiently strong policy supervision. However, a general target-free controller that reliably learns useful multi-step heterogeneous computation has not been established. The current evidence does not justify claiming a new universal computational primitive or superiority over modern Transformer, SSM, MoE, or dynamic-depth systems.**

The persistent-state substrate is a valid engineering/research architecture. The universal adaptive-control hypothesis remains unresolved rather than proven.

## 9. Research novelty conclusion

AEON's broad component list is **not novel in isolation**. The defensible potential contribution is the attempted integration of persistent state, heterogeneous transitions, policy-level compute allocation, memory, verification, and resource accounting under one substrate.

But integration alone is not sufficient for a scientific novelty claim. A publishable novelty claim would require a measurable advantage against strong contemporary adaptive-depth, MoE, hybrid, and resource-adaptive baselines under matched budgets and real execution.

That evidence does not yet exist.

## 10. Release implications

The software can be released as a **research reference implementation** if its README clearly states the above limitations.

It must not be released with claims such as:

- “Transformer killer”;
- “new fundamental architecture proven superior”;
- “universal adaptive intelligence”;
- “guaranteed lower latency/energy”;
- “first adaptive heterogeneous compute system.”

A future research generation should target direct comparisons against strong modern adaptive-depth and hybrid baselines on shared pretrained models, with real latency and energy measurements.

## 11. Final research disposition

**Research program: CLOSED at a scientifically meaningful checkpoint.**

Reason: the principal hypothesis has been tested through multiple architectural families, real and synthetic tasks, leakage audits, runtime studies, prior-art review, and both counterfactual and target-free control mechanisms. The remaining uncertainty is a new research program requiring substantially larger models/hardware and direct contemporary baselines, not another small patch to the current controller.


## Phase 4 final intrinsic reward-only control

A five-seed reward-only policy-gradient study tested target-free sequential heterogeneous computation without counterfactual labels. After correcting test-set fixed-policy selection, adaptive mean accuracy was 53.96% versus 51.24% for the training-selected fixed comparator, but adaptive proxy cost was 2.69 versus 2.60. This is a modest quality signal, not a compute-efficiency win, and closes the current intrinsic-controller formulation. See `AEON_SCIENTIFIC_FINAL.md`.
