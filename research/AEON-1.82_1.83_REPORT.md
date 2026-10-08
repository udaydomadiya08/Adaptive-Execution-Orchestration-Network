# AEON-1.82 / 1.83 — Persistent-State Controller Audit

## Purpose
Phase 2 tests whether AEON can combine the supported persistent-state substrate (1.81) with a target-free controller over reusable transitions.

## 1.82 — corrected target-free controller
The prior 1.81 controller implementation contained an accounting bug: the STOP action was encoded as the majority-class label rather than its actual majority-class accuracy. This made STOP artificially appear maximally valuable during controller training. 1.82 corrected the STOP utility and reran the same five-seed controlled task and real digits task.

### Controlled task
Fixed persistent A->B mean accuracy: ~84.74%.
Corrected adaptive controller: ~83.95% (approximately A-only behavior).
Across all five seeds, the controller selected A first for every test example and did not discover useful adaptive continuation.

### Digits task
The corrected controller also collapsed almost entirely to A-first behavior and did not improve the strongest fixed transition.

### Interpretation
1.82 is a negative controller result, but it also identifies and fixes an implementation-integrity bug in the previous controller. The persistent substrate result from 1.81 remains valid because it did not depend on this controller.

## 1.83 — regime-switching controller stress test
A fresh controlled task was created where the label mechanism changes with an input-observable regime: one regime emphasizes a linear evidence channel and the other a nonlinear channel. Five seeds were evaluated. The controller was trained only on the controller split using candidate transition outcomes available on that split. Test labels and unexecuted test transition outputs were not used for inference.

### Result
The fixed persistent sequences were approximately 89–91% accurate, while the adaptive controller reproduced the A-only specialist at approximately 87.8–88.8% on every seed. The controller selected A first for all 2,250 test examples on every seed. It therefore failed to exploit the instance-dependent regime structure.

## Scientific conclusion
The current Phase-2 evidence separates two questions:

1. **Does persistent reusable state carry additional useful information?** YES. 1.81 showed persistent A->B and B->A outperforming reset controls on all five seeds.
2. **Can the current target-free value controller learn when to invoke those reusable transitions?** NO. 1.82 and 1.83 both failed, including a deliberate regime-switching stress test.

This is not evidence that persistent computation is useless. It is evidence that the present controller/credit-assignment formulation is inadequate for exploiting the substrate.

## Branch decision
CLOSE the current first-generation persistent-state controller design. Do not continue with small classifier/capacity/threshold tweaks.

## Next major architectural question
The next AEON phase should investigate whether control should be **intrinsic to state transitions** (e.g. learned transition dynamics with an explicit continuation/value state) rather than a separate post-hoc classifier trained from counterfactual correctness labels. Any future controller must preserve strict target-free inference and automatic leakage checks.
