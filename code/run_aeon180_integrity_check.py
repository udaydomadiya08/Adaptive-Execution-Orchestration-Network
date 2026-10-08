#!/usr/bin/env python3
"""AEON phase-closure integrity check.

This checker is intentionally simple and fail-closed. It verifies that the frozen
phase dossier marks known leaked experiments as invalid and that the evidence
matrix contains the required positive/negative boundary cases.
"""
from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parent
report = (ROOT / "AEON-1.80_FINAL-CONSOLIDATION.md").read_text()
rows = list(csv.DictReader((ROOT / "AEON-1.80_EVIDENCE_MATRIX.csv").open()))

required_invalid = {"1.68", "1.70", "1.71", "1.74"}
invalid = {r["version"] for r in rows if r["status"] == "invalid"}
assert required_invalid <= invalid, (required_invalid, invalid)
assert "test target" in report.lower()
assert "PHASE COMPLETE" in report
assert any(r["version"] == "1.75" and r["status"] == "positive" for r in rows)
assert any(r["version"] == "1.79" and r["status"] == "negative" for r in rows)

print("AEON-1.80 integrity check: PASS")
print(f"Evidence rows: {len(rows)}")
print(f"Invalidated versions: {sorted(invalid)}")
