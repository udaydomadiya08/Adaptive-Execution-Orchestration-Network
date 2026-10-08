# AEON — Adaptive Persistent Computational Substrate

## Research status
**Scientific research program closed at a defensible checkpoint.**

AEON is a research architecture for persistent state, heterogeneous computation, adaptive sequencing, memory, verification, and resource-aware control.

### Strongest defensible result
Experiments establish that:
- heterogeneous capabilities can be complementary;
- persistent computational state can preserve useful information across transitions;
- selective computation can improve quality–proxy-cost tradeoffs on some tasks, especially with policy-value supervision;
- controller overhead can erase proxy savings in real wall-clock execution;
- target-free intrinsic multi-step control remains task-dependent and was not demonstrated as a universal advantage.

### What AEON does NOT claim
This release does not claim universal superiority over Transformers, modern LLMs, MoE systems, adaptive-depth methods, or frontier models. It does not claim universal latency/energy savings or a new fundamental computational primitive.

### Integrity
Historical experiments containing target leakage, precomputed unchosen branches, hard-coded expert outcomes, or oracle information were explicitly invalidated and are retained only as audit history.

### Frontier-model extension
The provider-neutral sidecar harness is included, but direct same-foundation-model frontier measurements were not performed in the final environment because no foundation-model runtime, cached model, or provider credential was available. These are therefore **not** presented as results.

## Reproduce
Run:

```bash
python3 code/run_aeon180_integrity_check.py
python3 code/aeon3_sidecar_v2.py
python3 code/aeon3_sidecar_v3.py
python3 code/aeon3_research_protocol.py
```

All four checks should pass.
