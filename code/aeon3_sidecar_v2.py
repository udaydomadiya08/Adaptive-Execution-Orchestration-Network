"""AEON-3 real sidecar experiment harness.

Scientific contract:
- Baseline and AEON use the exact same Provider implementation.
- AEON may invoke the provider only through explicit actions recorded in the trace.
- No candidate/branch precomputation is permitted.
- Every model call, tool call, token count, latency and cost is recorded.
- Persistent state is explicit JSON-serializable data; it is never hidden in provider state.
- The benchmark runner supplies task context; AEON cannot access target labels.

This file contains the substrate and accounting layer only. Provider adapters are deliberately
external so experiments cannot silently switch models or credentials.
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any, Callable, Dict, List, Optional, Protocol, Tuple
import json, time, hashlib, statistics


@dataclass
class Completion:
    text: str
    model: str
    input_tokens: int
    output_tokens: int
    reasoning_tokens: Optional[int]
    latency_s: float
    cost_usd: Optional[float]
    finish_reason: str = "stop"
    tool_calls: List[Dict[str, Any]] = field(default_factory=list)
    raw_usage: Dict[str, Any] = field(default_factory=dict)

    def validate(self):
        if not self.model: raise ValueError("model required")
        if min(self.input_tokens, self.output_tokens) < 0: raise ValueError("negative token count")
        if self.reasoning_tokens is not None and self.reasoning_tokens < 0: raise ValueError("negative reasoning tokens")
        if self.latency_s < 0: raise ValueError("negative latency")
        if self.cost_usd is not None and self.cost_usd < 0: raise ValueError("negative cost")
        return self


class Provider(Protocol):
    name: str
    def complete(self, messages: List[Dict[str, str]], tools: Optional[List[Dict[str, Any]]] = None,
                 effort: str = "fixed", budget: Optional[Dict[str, Any]] = None) -> Completion: ...


@dataclass
class PersistentState:
    goal: str
    facts: Dict[str, Any] = field(default_factory=dict)
    memory: Dict[str, str] = field(default_factory=dict)
    plan: List[str] = field(default_factory=list)
    completed_steps: List[str] = field(default_factory=list)
    uncertainty: float = 0.0
    verifier_status: str = "unverified"

    def snapshot(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Trace:
    task_id: str
    mode: str
    model: str
    actions: List[Dict[str, Any]]
    final_text: str
    total_input_tokens: int
    total_output_tokens: int
    total_reasoning_tokens: int
    total_model_calls: int
    total_tool_calls: int
    total_latency_s: float
    total_cost_usd: Optional[float]
    state_hashes: List[str]
    valid: bool = True
    invalid_reason: Optional[str] = None

    def validate(self):
        if self.mode not in {"baseline", "aeon"}: raise ValueError("bad mode")
        if self.total_model_calls != sum(1 for a in self.actions if a["kind"] == "model_call"):
            raise ValueError("model call accounting mismatch")
        if self.total_tool_calls != sum(1 for a in self.actions if a["kind"] == "tool_call"):
            raise ValueError("tool call accounting mismatch")
        return self


@dataclass
class Tool:
    name: str
    description: str
    fn: Callable[[Dict[str, Any]], Any]
    schema: Dict[str, Any]

    def execute(self, args: Dict[str, Any]) -> Tuple[Any, float]:
        t = time.perf_counter()
        result = self.fn(args)
        return result, time.perf_counter() - t


def _hash_state(state: PersistentState) -> str:
    raw = json.dumps(state.snapshot(), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


class BaselineRunner:
    """One direct completion with the same provider used by AEON."""
    def __init__(self, provider: Provider, effort: str = "fixed"):
        self.provider, self.effort = provider, effort

    def run(self, task_id: str, messages: List[Dict[str, str]], tools=None) -> Trace:
        t = time.perf_counter()
        c = self.provider.complete(messages, tools=tools, effort=self.effort)
        elapsed = time.perf_counter() - t
        c.validate()
        action = {"kind":"model_call", "index":0, "model":c.model,
                  "input_tokens":c.input_tokens, "output_tokens":c.output_tokens,
                  "reasoning_tokens":c.reasoning_tokens or 0, "latency_s":c.latency_s,
                  "cost_usd":c.cost_usd, "precomputed":False}
        tr = Trace(task_id, "baseline", c.model, [action], c.text,
                   c.input_tokens, c.output_tokens, c.reasoning_tokens or 0, 1,
                   len(c.tool_calls), elapsed, c.cost_usd, [], True, None)
        return tr.validate()


class AEONRunner:
    """Minimal real sidecar: persistent state + sequential model/tool transitions.

    The model itself decides whether another transition is necessary. No alternate model
    completion is computed merely to estimate its value. A hard budget prevents unbounded loops.
    """
    def __init__(self, provider: Provider, tools: Dict[str, Tool], max_model_calls: int = 6,
                 effort: str = "fixed"):
        self.provider, self.tools = provider, tools
        self.max_model_calls, self.effort = max_model_calls, effort

    def _tool_specs(self):
        return [{"name":t.name,"description":t.description,"parameters":t.schema} for t in self.tools.values()]

    def run(self, task_id: str, messages: List[Dict[str, str]], goal: str,
            memory: Optional[Dict[str, str]]=None) -> Trace:
        state = PersistentState(goal=goal, memory=dict(memory or {}))
        actions: List[Dict[str, Any]] = []
        state_hashes = [_hash_state(state)]
        history = list(messages)
        total_in = total_out = total_reason = 0
        total_latency = 0.0
        total_cost: Optional[float] = 0.0
        model_name = "unknown"
        final = ""

        system = {
            "role":"system",
            "content":(
                "You are operating inside the AEON substrate. Maintain the supplied persistent "
                "state mentally and act sequentially. You may answer directly or request a tool. "
                "Never assume unseen tool results. When you have enough evidence, give the final answer. "
                "If uncertain, say so."
            )
        }
        history = [system] + history

        for step in range(self.max_model_calls):
            t = time.perf_counter()
            c = self.provider.complete(history, tools=self._tool_specs(), effort=self.effort,
                                       budget={"remaining_model_calls": self.max_model_calls-step})
            elapsed = time.perf_counter() - t
            c.validate(); model_name = c.model
            total_in += c.input_tokens; total_out += c.output_tokens
            total_reason += c.reasoning_tokens or 0; total_latency += elapsed
            if c.cost_usd is not None: total_cost = (total_cost or 0.0) + c.cost_usd
            actions.append({"kind":"model_call","index":step,"model":c.model,
                            "input_tokens":c.input_tokens,"output_tokens":c.output_tokens,
                            "reasoning_tokens":c.reasoning_tokens or 0,"latency_s":c.latency_s,
                            "cost_usd":c.cost_usd,"precomputed":False})

            final = c.text
            if not c.tool_calls:
                state.verifier_status = "pending"
                # Provider-neutral convention: a final answer is a terminal state.
                state.completed_steps.append("model_answer")
                state_hashes.append(_hash_state(state))
                break

            for tc in c.tool_calls:
                name = tc.get("name")
                args = tc.get("arguments") or {}
                if name not in self.tools:
                    raise ValueError(f"provider requested unavailable tool: {name}")
                result, tool_latency = self.tools[name].execute(args)
                actions.append({"kind":"tool_call","name":name,"arguments":args,
                                "latency_s":tool_latency,"result_digest":hashlib.sha256(
                                    json.dumps(result,sort_keys=True,default=str).encode()).hexdigest()[:16]})
                state.facts[name] = result
                state.completed_steps.append(name)
                history.append({"role":"assistant","content":c.text})
                history.append({"role":"tool","name":name,"content":json.dumps(result,default=str)})
                state_hashes.append(_hash_state(state))

        else:
            state.verifier_status = "budget_exhausted"
            actions.append({"kind":"budget_exhausted"})

        # Reject hidden fallback semantics.
        for a in actions:
            if a.get("kind") == "model_call" and a.get("precomputed"):
                return Trace(task_id,"aeon",model_name,actions,final,total_in,total_out,total_reason,
                             sum(a.get("kind")=="model_call" for a in actions),
                             sum(a.get("kind")=="tool_call" for a in actions),total_latency,total_cost,
                             state_hashes,False,"precomputed model branch detected")
        tr = Trace(task_id,"aeon",model_name,actions,final,total_in,total_out,total_reason,
                   sum(a.get("kind")=="model_call" for a in actions),
                   sum(a.get("kind")=="tool_call" for a in actions),total_latency,total_cost,
                   state_hashes,True,None)
        return tr.validate()


def save_trace(path: str, trace: Trace):
    with open(path,"w") as f: json.dump(asdict(trace),f,sort_keys=True,indent=2)


if __name__ == "__main__":
    class DeterministicProvider:
        name="deterministic-foundation"
        def complete(self,messages,tools=None,effort="fixed",budget=None):
            content = messages[-1].get("content","")
            if "use_tool" in content and tools:
                return Completion("",self.name,50,4,0,0.001,0.0,tool_calls=[{"name":tools[0]["name"],"arguments":{}}])
            return Completion("FINAL: " + content[-32:],self.name,50,8,0,0.001,0.0)

    p=DeterministicProvider()
    tool=Tool("lookup","deterministic lookup",lambda a:{"answer":42},{"type":"object","properties":{}})
    task=[{"role":"user","content":"use_tool then solve this task"}]
    b=BaselineRunner(p).run("smoke",task)
    a=AEONRunner(p,{tool.name:tool}).run("smoke",task,"smoke goal")
    assert b.model == a.model
    assert a.valid and a.total_model_calls == 2 and a.total_tool_calls == 1
    print("AEON-3 sidecar v2: PASS")
    print(json.dumps({"baseline_calls":b.total_model_calls,"aeon_calls":a.total_model_calls,"aeon_tools":a.total_tool_calls},indent=2))
