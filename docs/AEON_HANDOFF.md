# AEON HANDOFF — PHASE 2 CONTROLLER BRANCH CLOSED AT 1.83

## Phase 1 status
Phase 1 adaptive-routing/policy-value research remains complete. Valid evidence and invalidated results are documented in AEON-1.80.

## Phase 2 status
### 1.81 — persistent substrate proof-of-mechanism
Persistent state is useful: persistent A->B and B->A beat reset-to-h0 controls on all five seeds by ~1.47pp and ~1.87pp respectively. This isolates a genuine reusable-computation signal.

### 1.82 — corrected target-free controller
The first controller implementation had a STOP utility bug. After correcting it, the controller collapsed to A-first and failed to improve fixed persistent computation. This is a valid negative controller result.

### 1.83 — regime-switching stress test
A fresh task with instance-dependent linear/nonlinear regimes was used to test whether the controller could select different reusable transitions. It still collapsed to A-first on all five seeds. Negative result.

## Current scientific conclusion
**Persistent computational state: supported as a proof-of-mechanism.**
**Current target-free controller design: rejected/closed.**

Do not produce tiny 1.84/1.85 controller-capacity/threshold variants. The next work must change the control architecture itself.

## Next major direction
Investigate intrinsic control in the recurrent substrate: state carries both task information and a learned continuation/value representation; transition choice should be generated from that state rather than a separately trained post-hoc classifier. Compare against fixed persistent sequences, reset controls, and an oracle. Maintain automatic target-leakage sentinels and real execution accounting from the start.

## Files
- AEON-1.82_1.83_REPORT.md
- run_aeon182_persistent_controller.py
- run_aeon183_regime_controller.py
- results/aeon182_persistent_controller.json
- results/aeon183_regime_controller.json
- AEON-1.81_REPORT.md
- AEON-1.80_FINAL-CONSOLIDATION.md
