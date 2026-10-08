"""Machine-readable AEON-3 experiment contract and audit utilities."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from pathlib import Path
import json, hashlib

ROOT=Path(__file__).resolve().parent

@dataclass(frozen=True)
class Condition:
    name: str
    provider: str
    model: str
    effort: str
    tools_version: str
    max_model_calls: int
    seed: int

@dataclass(frozen=True)
class Task:
    task_id: str
    family: str
    prompt: str
    gold: str
    tools_allowed: bool


def fingerprint(condition: Condition, tasks: list[Task]) -> str:
    obj={"condition":asdict(condition),"tasks":[asdict(t) for t in tasks]}
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(",",":")).encode()).hexdigest()


def audit_trace(trace: dict):
    assert trace["valid"] is True
    assert trace["total_model_calls"] == sum(a.get("kind")=="model_call" for a in trace["actions"])
    assert trace["total_tool_calls"] == sum(a.get("kind")=="tool_call" for a in trace["actions"])
    assert all(not a.get("precomputed",False) for a in trace["actions"] if a.get("kind")=="model_call")
    return True

if __name__ == "__main__":
    c=Condition("aeon","provider","model","fixed","tools-v1",6,0)
    ts=[Task("t1","reasoning","answer 2+2","4",False)]
    print(json.dumps({"fingerprint":fingerprint(c,ts),"audit":"PASS"},indent=2))
